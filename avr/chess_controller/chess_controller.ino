/* 
 * Settings for the board:
 * DB-Series
 * AVR64DB64 (optiboot)
 * Clock Speed: Min 24 MHz, internal
 * Bootloader Serial port: PC0, PC1
 * MVIO: Enabled
 * 
*/ 

#define PIECE_TAKEN   't'
#define PIECE_PLACED  'p'
#define SET_LED       's'
#define CLR_LED       'k'
#define TGL_LED       'x'
#define GET_LEDS      'l'
#define GET_REEDS     'r'
#define CLR_LED_LINE  'n'
#define CLR_LED_BOARD 'o'
#define GET_BOARD     'b'
#define BOARD_LAYOUT  'v'
#define ERROR_FLAG    'e'

#define FW_UPLOAD     "DFU" // Device Firmware Update

#define CURR_LINE     GPR.GPR2
#define LINE_REED     GPR.GPR1
#define ACQ_STATUS    GPR.GPR0

#define REED_VPORT    VPORTE
#define LED_VPORT     VPORTB
#define COM_VPORT     VPORTA


#define DELTIME 100

uint8_t led_matrix[] = {
  0b10000001,
  0b01000010,
  0b00100100,
  0b00011000,
  0b00011000,
  0b00100100,
  0b01000010,
  0b10000001,
};


#ifdef Serial
  #undef Serial
  #define Serial Serial1
#endif


uint8_t reed_matrix[8][8] = {};
// Current state of the Piece at that position. 
//~50 means its currently not there. At >100 it flips
//~190 means its currently there. At <140 it flips.

uint8_t reed_bool[8] = {};
// Each Bit represents the current state of the reed Contact. (1= Active)




uint8_t all_lines_counter = 0;

uint8_t* current_leds = led_matrix;

void setup() {
  PORTA.DIR = 0xFF; // Set all Common Pins to OUTPUT
  PORTB.DIR = 0xFF; // Set all LED Pins to OUTPUT

  PORTE.PINCONFIG = PORT_INVEN_bm | PORT_INLVL_bm | PORT_PULLUPEN_bm; // Set all PORTE Pins to Input PULLUP and invert them to get positive logic (1 = piece)  
  PORTE.PINCTRLUPD = 0xFF;

  TCB4.INTFLAGS = 0x03; // Clear ISR Flags
  TCB4.INTCTRL = 0x02;  // Overflow ISR
  //TCB4.CCMP = (F_CPU/2) / (8*40); // 320 LPS
  // 24MHz / 2 = 12MHz
  // 12MHz / 46875 = 256
  // 256 / 8 lines = 32 FPS 
  TCB4.CCMP = 46875;
  TCB4.CTRLA = TCB_CLKSEL_DIV2_gc | TCB_ENABLE_bm;
  
  digitalWriteFast(PIN_PD0, HIGH);  // "disable" LED
  pinConfigure(PIN_PD0, (PIN_DIR_OUT | PIN_INVERT_ON | PIN_ISC_DISABLE));
  digitalWriteFast(PIN_PA0, HIGH);  // init FET loop
  CURR_LINE = 0x00;
  Serial.begin(115200);
  
  Serial.println("Setup Done");
  digitalWriteFast(PIN_PD0, HIGH);  // "Enable" LED

  boot_splash();
}

uint8_t serial_input_buffer[8] = {};
uint8_t serial_position = 0;

void loop() {
  handle_reed_scan();

  while (Serial.available()) {
    uint8_t ch = Serial.read();

    if (ch == '\r')
      continue;
    else if (ch == '\n') {
      serial_position = 0;
      uint8_t cmd = serial_input_buffer[0];
      uint8_t letter = serial_input_buffer[1];
      uint8_t number = serial_input_buffer[2] - '0';

      if (letter > 'Z') { // transform letter to number
        letter -= 'a';
      } else {
        letter -= 'A';
      }
      number -= 1; // adjust 1~8 to 0~7

      if (number < 8) {   // Try to handle LED commands first, it's mostly those 
        if (letter < 8) {
          uint8_t bit_pos = 1 << letter;
          if (cmd == SET_LED) {
            led_matrix[number] |= bit_pos;
            break;
          } else if (cmd == CLR_LED) {
            led_matrix[number] &= ~(bit_pos);
            break;
          } else if (cmd == TGL_LED) {
            led_matrix[number] ^= bit_pos;
            break;
          }
        }
      }


      if (cmd == GET_LEDS) {
        print_led_board();
      } else if (cmd == GET_REEDS) {
        print_reed_board();
      } else if (cmd == CLR_LED_BOARD) {
        memset(led_matrix, 0x00, 8);
      } else if (cmd == CLR_LED_LINE) {
        if (number < 8) { // n*1
          led_matrix[number] = 0x00;
        }
      } else if (cmd == GET_BOARD) {        // prints "va1;a2;b3;...;\n" where a piece is placed
        uint8_t *reed = &reed_matrix[0][0];
        Serial.write(BOARD_LAYOUT);
        for (uint8_t line = '1'; line <= '8'; line++) {
          for (uint8_t col = 'a'; col <= 'h'; col++) {
            if (*reed > 120) {
              Serial.write(col);
              Serial.write(line);
              Serial.write(";");
            }
            reed++;
          }
        }
        Serial.write("\n");
      } else if (memcmp(serial_input_buffer, "DFU", 3) == 0) {
        Serial.write("d");
        Serial.write("f");
        Serial.write("u");
        Serial.write("\n");
        Serial.flush();
        _PROTECTED_WRITE(RSTCTRL.SWRR, 1); // Trigger Software Reset, bootloader will handle the rest
      }
    } else {
      serial_input_buffer[serial_position++] = ch;
      if (serial_position > 4) {
        Serial.println(ERROR_FLAG);
        serial_position = 0;
      }
    }
  }
}

// change reed_matrix according to reed_bool
// increase if active, decrease when inactive
// no overflow (>150) or underflow (<50)

void handle_reed_scan(void) {
  if (ACQ_STATUS & 0x01) {                    // all lines scanned
    ACQ_STATUS &= ~0x01;                      // clear Flag
    uint8_t *pNewReed = &reed_bool[0];        // contains the current state of the reed contacts
    uint8_t *pOldReed = &reed_matrix[0][0];   // contains a byte per reed as a counter to low-pass filter
    for (uint8_t i = 0; i < 8; i++) {         // go through every line
      uint8_t newReed = *(pNewReed++);
      for (uint8_t j = 0; j < 8; j++) {       // go through each column
        uint8_t value = *pOldReed;
        //value = reed_matrix[i][j]
        //newReed = reed_bool[i] >> j
        if(newReed & 0x01) {                  // if figure placed
          if (value < 200)                    // upper limit of 190 + 10
            *pOldReed = value + 1;            // count up
        } else {                              // no figure placed
          if (value > 40)                     // lower limit of 50 - 10
            *pOldReed = value - 1;            // count down
        }
        pOldReed++;
        newReed /= 2;
      }
    }
    notify_takes_places();
  }
}

// Check if reed_matrix has to flip, else reset to base value (30 if no piece is there, 170 otherwise)
void notify_takes_places(void) {
  static uint8_t all_lines_counter = 0;
  all_lines_counter += 1;
  if (all_lines_counter >= 60) {    // 60 iterations, if 50 were positive, a flip occurs
    all_lines_counter = 0;
    uint8_t *reed = &reed_matrix[0][0];
    
    for (uint8_t line = '1'; line <= '8'; line++) {
      for (uint8_t col = 'a'; col <= 'h'; col++) {
        uint8_t counter = *reed;
        if (counter > 120) {       // count up
          if (counter <= 140) {     // counted "50 down"
            counter = 50;           // piece removed
            Serial.write(PIECE_TAKEN);
            Serial.write(col);
            Serial.write(line);
            Serial.write('\n');
          } else {
            counter = 190;          // fall back to base
          }
        } else {
          if (counter >= 100) {     // counted "50 up"
            counter = 190;            // piece touched
            Serial.write(PIECE_PLACED);
            Serial.write(col);
            Serial.write(line);
            Serial.write('\n');
          } else {
            counter = 50;
          }
        }
        *reed = counter;
        reed++;
      }
    }
  }
}

void print_led_board(void) {
  for (uint8_t line_num = '8'; line_num >= '1'; line_num--) {
    Serial.write(line_num);
    Serial.print(": ");
    uint8_t led_line = current_leds[line_num-'1'];
    for (uint8_t j = 0; j < 8; j++) {
      uint8_t ch = '_';
      if (led_line & 0x01) {
        ch = 'x';
      }
      led_line >>= 1;
      Serial.write(ch);
      Serial.write(' ');
    }
    Serial.println();
  }
  Serial.println("   A B C D E F G H");
}


void print_reed_board(void) {
  for (uint8_t line_num = '8'; line_num >= '1'; line_num--) {
    Serial.write(line_num);
    Serial.print(": ");
    uint8_t *reed_line = reed_matrix[line_num-'1'];
    for (uint8_t j = 0; j < 8; j++) {
      if (*reed_line > 120)
        Serial.print('x');
      else
        Serial.print('_');
      Serial.write(' ');
      reed_line++;
    }
    Serial.println();
  }
  Serial.println("   A B C D E F G H");
}

void boot_splash(void) {
  uint8_t boot_led [] = {0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  uint8_t field_cnt = 0;
  uint8_t move_cnt = 0;
  current_leds = boot_led;
  while(Serial.available() == 0) {
    if (ACQ_STATUS & 0x01) {
      ACQ_STATUS &= ~0x01;
      field_cnt++;
      if (field_cnt >= 250) {
        field_cnt = 0;
        print_led_board();
        for (uint8_t i = 8; i > 0; i--) {
          boot_led[i] = boot_led[i-1];
        }
        boot_led[0] >>= 1;
        move_cnt++;
        if (move_cnt > 15)  {
          break;
        }
      }
    }
  }
  current_leds = led_matrix;
}


ISR(TCB4_INT_vect) {
  uint8_t line = CURR_LINE;           // use GPIO Reg for faster access
  uint8_t com = COM_VPORT.OUT << 1;   // get current active com transistor
  reed_bool[line] = REED_VPORT.IN;    // save reed info
  line += 1;
  COM_VPORT.OUT = 0x00;               // disable com Transistors
  if (com == 0x00) {
    LED_VPORT.OUT = current_leds[0];  // load new LED state
    COM_VPORT.OUT = 0x01;             // enable first com transistor
    ACQ_STATUS |= 0x01;               // indicator for "all 8"
    CURR_LINE = 0x00;
    VPORTD.IN |= 0x01;                // activity PD0 (toggle)
  } else {
    LED_VPORT.OUT = current_leds[line];  // load new LED state
    COM_VPORT.OUT = com;              // enable next com transistor
    CURR_LINE = line;                   // update Current line
  }
  TCB4.INTFLAGS = 0x03;
}

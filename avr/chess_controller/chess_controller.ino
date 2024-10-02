#define PIECE_TAKEN   't'
#define PIECE_PLACED  'p'
#define SET_LED       's'
#define CLR_LED       'k'
#define TGL_LED       'x'

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
uint8_t new_reed[8] = {};

uint8_t serial_buffer[8] = { 0x00 };
uint8_t serial_position = 0;


uint8_t all_lines_counter = 0;

uint8_t* current_leds = led_matrix;

void setup() {
  PORTA.DIR = 0xFF; // Set all Common Pins to OUTPUT
  PORTB.DIR = 0xFF; // Set all LED Pins to OUTPUT

  PORTE.PINCONFIG = PORT_INVEN_bm | PORT_PULLUPEN_bm; // Set all PORTE Pins to Input PULLUP and invert them to get positive logic (1 = piece)  
  PORTE.PINCTRLUPD = 0xFF;

  TCB4.INTFLAGS = 0x03; // Clear ISR Flags
  TCB4.INTCTRL = 0x02;  // Overflow ISR
  //TCB4.CCMP = (F_CPU/2) / (8*40); // 320 LPS
  TCB4.CCMP = 65000;
  TCB4.CTRLA = TCB_CLKSEL_DIV2_gc | TCB_ENABLE_bm;
  
 
  digitalWriteFast(PIN_PD0, HIGH);  // onboard LED
  pinMode(PIN_PD0, OUTPUT);
  digitalWriteFast(PIN_PA0, HIGH);  // init FET loop
  CURR_LINE = 0x00;
  Serial.begin(1000000);
  
  Serial.println("Setup Done");
  digitalWriteFast(PIN_PD0, LOW);

  boot_splash();
}

void loop() {
  uint8_t output_buffer[5] = {};  // keep in stack for faster access
  /*
  cli();                          // ISR guard
  uint8_t flags = ACQ_STATUS;
  uint8_t new_reed = LINE_REED;
  uint8_t line = CURR_LINE;
  sei(); */
  /*
  if (flags & 0x02) {    // one line scanned
    ACQ_STATUS &= ~0x02;  // clear Flag
    uint8_t *old_reed = reed_matrix[line];
        Serial.println(line);
    
    for (uint8_t i = 0; i < 8; i++) {
      uint8_t value = old_reed[i];
      if(new_reed & 0x01) {
        if (value < 150)
          value += 1;
      } else {
        if (value > 50)
          value -= 1;
      }
      old_reed[i] = value;
      new_reed >>= 1;
    }
  }
  */
  if (ACQ_STATUS & 0x01) {                   // all lines scanned
    ACQ_STATUS &= ~0x01;                // clear Flag
    uint8_t *pNewReed = &new_reed[0];
    uint8_t *pOldReed = &reed_matrix[0][0];
    for (uint8_t i = 0; i < 8; i++) {
      uint8_t newReed = *(pNewReed++);
      for (uint8_t j = 0; j < 8; j++) {
        uint8_t value = *pOldReed;
        if(newReed & 0x01) {
          if (value < 150)
            value += 1;
        } else {
          if (value > 50)
            value -= 1;
        }
        *(pOldReed++) = value;
        newReed >>= 1;
      }
    }
    if (++all_lines_counter >= 24) {    // 24 iterations
      all_lines_counter = 0;
      uint8_t *reed = &reed_matrix[0][0];
      
      for (uint8_t line = '1'; line <= '8'; line++) {
        /*
        if (line == '7') {
          Serial.print(reed_matrix[7][0]);
          Serial.print(reed_matrix[7][1]);
          Serial.print(reed_matrix[7][2]);
          Serial.print(reed_matrix[7][3]);
          Serial.print(reed_matrix[7][4]);
          Serial.print(reed_matrix[7][5]);
          Serial.print(reed_matrix[7][6]);
          Serial.println(reed_matrix[7][7]);
        }
        */
        for (uint8_t col = 'a'; col <= 'h'; col++) {
          uint8_t counter = *reed;
          if (counter >= 100) {       // count up
            if (counter <= 120) {     // counted "20 down"
              counter = 60;           // piece removed
              output_buffer[0] = PIECE_TAKEN;
              output_buffer[1] = col;
              output_buffer[2] = line;
              output_buffer[3] = '\n';
              output_buffer[4] = 0x00;
              Serial.print((char *)output_buffer);
            } else {
              counter = 140;          // fall back to base
            }
          } else {
            if (counter >= 80) {      // counted "20 up"
              counter = 140;          // piece touched
              output_buffer[0] = PIECE_PLACED;
              output_buffer[1] = col;
              output_buffer[2] = line;
              output_buffer[3] = '\n';
              output_buffer[4] = 0x00;
              Serial.print((char *)output_buffer);
            } else {
              counter = 60;
            }
          }
          *reed = counter;
          reed++;
        }
      }
    }

  }
  while (Serial.available()) {
    uint8_t ch = Serial.read();

    if (ch == '\r')
      continue;
    else if (ch == '\n') {
      serial_position = 0;
      uint8_t cmd = serial_buffer[0];
      uint8_t letter = serial_buffer[1];
      uint8_t number = serial_buffer[2] - '0';

      if (letter > 'Z') {
        letter -= 'a';
      } else {
        letter -= 'A';
      }
      number -= 1; // adjust 1~8 to 0~7
      uint8_t bit_pos = 1 << letter;
      if (cmd == 'p') {
          print_led_board();
      } else if (cmd == 'P') {
          print_reed_board();
      } else {
        if (letter < 8 && number < 8) {
          if (cmd == SET_LED) {
            led_matrix[number] |= bit_pos;
          } else if (cmd == CLR_LED) {
            led_matrix[number] &= ~(bit_pos);
          } else if (cmd == TGL_LED) {
            led_matrix[number] ^= bit_pos;
          }
        }
      }
    } else {
      serial_buffer[serial_position++] = ch;
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
      Serial.print(*reed_line);
      Serial.write(' ');
      reed_line++;
    }
    Serial.println();
  }
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
  uint8_t line = CURR_LINE + 1;       // use GPIO Reg for faster access
  uint8_t com = COM_VPORT.OUT << 1;   // get current active com transistor
  new_reed[line - 1]   = REED_VPORT.IN; // save reed info
  COM_VPORT.OUT = 0x00;               // disable com Transistors
  if (com == 0x00) {
    COM_VPORT.OUT = 0x01;             // enable first com transistor
    LED_VPORT.OUT = current_leds[0];  // load new LED state
    ACQ_STATUS |= 0x01;               // indicator for "all 8"
    CURR_LINE = 0x00;
    VPORTD.IN |= 0x01;                // activity PD0
  } else {
    COM_VPORT.OUT = com;              // enable next com transistor
    LED_VPORT.OUT = current_leds[line];  // load new LED state
    //ACQ_STATUS |= 0x02;               // indicator for new Line
    CURR_LINE = line;                   // update Current line
  }
  TCB4.INTFLAGS = 0x03;
}

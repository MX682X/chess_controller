#define BORDER 17
#define FIELD 25
LV_IMAGE_DECLARE(Board);

lv_obj_t* boardimage;

LV_IMAGE_DECLARE(White_Bishop);
LV_IMAGE_DECLARE(White_King);
LV_IMAGE_DECLARE(White_Knight);
LV_IMAGE_DECLARE(White_Pawn);
LV_IMAGE_DECLARE(White_Queen);
LV_IMAGE_DECLARE(White_Rook);

LV_IMAGE_DECLARE(Black_Bishop);
LV_IMAGE_DECLARE(Black_King);
LV_IMAGE_DECLARE(Black_Knight);
LV_IMAGE_DECLARE(Black_Pawn);
LV_IMAGE_DECLARE(Black_Queen);
LV_IMAGE_DECLARE(Black_Rook);




// Function to draw a chess piece on the board
void draw_piece(lv_obj_t* parent, int x, int y, char piece) {
  // Here we assume you have pre-loaded images for the chess pieces.
  // You'll need to adjust based on your piece representation (image files, Unicode characters, etc.).
  const lv_image_dsc_t* piece_img = NULL;

  // Select piece image based on the character
  switch (piece) {
    case 'K': piece_img = &White_King; break;
    case 'Q': piece_img = &White_Queen; break;
    case 'R': piece_img = &White_Rook; break;
    case 'B': piece_img = &White_Bishop; break;
    case 'N': piece_img = &White_Knight; break;
    case 'P': piece_img = &White_Pawn; break;
    case 'k': piece_img = &Black_King; break;
    case 'q': piece_img = &Black_Queen; break;
    case 'r': piece_img = &Black_Rook; break;
    case 'b': piece_img = &Black_Bishop; break;
    case 'n': piece_img = &Black_Knight; break;
    case 'p': piece_img = &Black_Pawn; break;
    default: return;  // Skip empty squares
  }

  // Create an image object for the piece and set its source
  lv_obj_t* img = lv_img_create(parent);
  lv_img_set_src(img, piece_img);

  // Set the position of the image (center it in the square)
  lv_obj_set_pos(img, x * FIELD + BORDER, y * FIELD + BORDER);
}


void lv_create_Boardtab(lv_obj_t* parent) {
  boardimage = lv_image_create(parent);
  lv_obj_set_size(boardimage, 240, 240);
  lv_image_set_src(boardimage, &Board);
  lv_image_set_scale(boardimage, 200);
  lv_obj_center(boardimage);
}

void set_board_fen(const char* fen) {
  //Delete Old pieces

  while(lv_obj_get_child_count(boardimage) != 0 ){
    lv_obj_delete(lv_obj_get_child(boardimage, 0));
  }


  // Parse the FEN string and place the pieces
  int row = 0;
  int col = 0;
  for (int i = 0; fen[i] != '\0'; i++) {
    char ch = fen[i];

    if (ch == ' ') {
      // Skip spaces (after the board state in FEN)
      continue;
    } else if (ch == '/') {
      // End of row in FEN, move to next row
      row++;
      col = 0;
    } else if (ch >= '1' && ch <= '8') {
      // Empty squares (number represents how many empty squares to skip)
      col += ch - '0';  // Increment col by the number of empty squares
    } else {
      // Piece found, draw it on the board
      draw_piece(boardimage, col, row, ch);
      col++;  // Move to the next square in the row
    }
  }
}

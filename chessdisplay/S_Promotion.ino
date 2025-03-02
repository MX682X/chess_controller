char queen_Text[] = "queen";
char rook_Text[] = "rook";
char bishop_Text[] = "bishop";
char knight_Text[] = "knight";

void lv_create_promotion(lv_obj_t* parent, bool black) {

  //Top Text
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "In was soll der Bauer \n Umgewandelt werden?");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_18, 0);

  lv_obj_align(text_label, LV_ALIGN_TOP_MID, 0, 10);


  //Buttons

  static lv_style_t imgstyle;
  lv_style_init(&imgstyle);
  lv_style_set_width(&imgstyle, 50);
  lv_style_set_height(&imgstyle, 50);


  //Queen Button
  lv_obj_t* queen_btn = lv_button_create(parent);
  lv_obj_add_event_cb(queen_btn, promo_callback, LV_EVENT_CLICKED, queen_Text);
  lv_obj_align(queen_btn, LV_ALIGN_CENTER, -50, -10);

  lv_obj_t* queen_image = lv_image_create(queen_btn);
  if (black) {
    LV_IMAGE_DECLARE(Black_Queen);
    lv_image_set_src(queen_image, &Black_Queen);
  } else {
    LV_IMAGE_DECLARE(White_Queen);
    lv_image_set_src(queen_image, &White_Queen);
  }
  lv_obj_add_style(queen_image, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(queen_image, 512);

  //Rook Button
  lv_obj_t* rook_btn = lv_button_create(parent);
  lv_obj_add_event_cb(rook_btn, promo_callback, LV_EVENT_CLICKED, rook_Text);
  lv_obj_align(rook_btn, LV_ALIGN_CENTER, 50, -10);

  lv_obj_t* rook_image = lv_image_create(rook_btn);
  if (black) {
    LV_IMAGE_DECLARE(Black_Rook);
    lv_image_set_src(rook_image, &Black_Rook);
  } else {
    LV_IMAGE_DECLARE(White_Rook);
    lv_image_set_src(rook_image, &White_Rook);
  }
  lv_obj_add_style(rook_image, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(rook_image, 512);

  //Bishop Button
  lv_obj_t* bishop_btn = lv_button_create(parent);
  lv_obj_add_event_cb(bishop_btn, promo_callback, LV_EVENT_CLICKED, bishop_Text);
  lv_obj_align(bishop_btn, LV_ALIGN_BOTTOM_MID, -50, -10);

  lv_obj_t* bishop_image = lv_image_create(bishop_btn);

  if (black) {
    LV_IMAGE_DECLARE(Black_Bishop);
    lv_image_set_src(bishop_image, &Black_Bishop);
  } else {
    LV_IMAGE_DECLARE(White_Bishop);
    lv_image_set_src(bishop_image, &White_Bishop);
  }
  lv_obj_add_style(bishop_image, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(bishop_image, 512);

  //Knight Button
  lv_obj_t* knight_btn = lv_button_create(parent);
  lv_obj_add_event_cb(knight_btn, promo_callback, LV_EVENT_CLICKED, knight_Text);
  lv_obj_align(knight_btn, LV_ALIGN_BOTTOM_MID, 50, -10);

  lv_obj_t* knight_image = lv_image_create(knight_btn);
  if (black) {
    LV_IMAGE_DECLARE(Black_Knight);
    lv_image_set_src(knight_image, &Black_Knight);
  } else {
    LV_IMAGE_DECLARE(White_Knight);
    lv_image_set_src(knight_image, &White_Knight);
  }
  lv_obj_add_style(knight_image, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(knight_image, 512);
}


static void promo_callback(lv_event_t* e) {
  Serial.print("Promotion:");
  Serial.println((char*)lv_event_get_user_data(e));
}

void transition_s_Promotion(bool black) {
  if (activeScene == S_Promotion) {
    return;
  }

  lv_obj_t* scene = lv_obj_create(NULL);
  lv_create_promotion(scene,black);
  lv_screen_load_anim(scene, LV_SCR_LOAD_ANIM_MOVE_TOP, 1000, 0, true);
  activeScene = S_Promotion;
}
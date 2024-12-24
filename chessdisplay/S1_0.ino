void lv_create_s_1_0(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Choose your Fighter!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_TOP_MID, 0, 10);


  static lv_style_t imgstyle;
  lv_style_init(&imgstyle);
  lv_style_set_width(&imgstyle, 50);
  lv_style_set_height(&imgstyle, 50);


  lv_obj_t* bk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(bk_btn, bkbtn_callback, LV_EVENT_CLICKED, NULL);
  lv_obj_align(bk_btn, LV_ALIGN_LEFT_MID, 5, 0);

  LV_IMAGE_DECLARE(bK_1_0);
  lv_obj_t* bkimg = lv_image_create(bk_btn);
  lv_image_set_src(bkimg, &bK_1_0);
  lv_obj_add_style(bkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(bkimg, 512);



  lv_obj_t* wk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(wk_btn, wkbtn_callback, LV_EVENT_CLICKED, NULL);
  lv_obj_align(wk_btn, LV_ALIGN_RIGHT_MID, -5, 0);

  LV_IMAGE_DECLARE(wK_1_0);
  lv_obj_t* wkimg = lv_image_create(wk_btn);
  lv_image_set_src(wkimg, &wK_1_0);
  lv_obj_add_style(wkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(wkimg, 512);



  lv_obj_t* wbk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(wbk_btn, wbkbtn_callback, LV_EVENT_CLICKED, NULL);
  lv_obj_align(wbk_btn, LV_ALIGN_CENTER, 0, 0);

  LV_IMAGE_DECLARE(wbK_1_0);
  lv_obj_t* wbkimg = lv_image_create(wbk_btn);
  lv_image_set_src(wbkimg, &wbK_1_0);
  lv_obj_add_style(wbkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(wbkimg, 490);
}

static void bkbtn_callback(lv_event_t * e) {
  Serial.println("COM:BTN1_0:CB");
}

static void wkbtn_callback(lv_event_t * e) {
  Serial.println("COM:BTN1_0:CW");
}

static void wbkbtn_callback(lv_event_t * e) {
  Serial.println("COM:BTN1_0:CR");
}

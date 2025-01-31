//Endscreen

void lv_create_s_1_2_b(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Sieg fuer Schwarz!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_CENTER, 0, 0);
}

void lv_create_s_1_2_w(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Sieg fuer Weis!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_CENTER, 0, 0);
}

void lv_create_s_1_2_r(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Remie!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_CENTER, 0, 0);
}

void lv_create_s_1_2_p(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Patt!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_CENTER, 0, 0);
}
void transition_s_1_2(String type) {
  lv_obj_t* scene_1_2 = lv_obj_create(NULL);

  if (type == "r") {
    lv_create_s_1_2_r(scene_1_2);
  } else if (type == "p") {
    lv_create_s_1_2_p(scene_1_2);
  } else if (type == "w") {
    lv_create_s_1_2_w(scene_1_2);
  } else if (type == "b") {
    lv_create_s_1_2_b(scene_1_2);
  }else{
    LV_LOG_WARN("Invalid game outcome. only b,w,r,p are allowed");
    lv_obj_del(scene_1_2);
    return;
  }
    lv_screen_load_anim(scene_1_2, LV_SCR_LOAD_ANIM_MOVE_TOP, 1000, 0, true);
  activeScene = S_End;
}

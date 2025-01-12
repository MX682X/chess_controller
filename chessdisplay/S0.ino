// Scene 0 (Disconnectet Screen)

void lv_create_s_0(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Disconnected!");
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);
}

void transition_s_0() {
  if (activeScene == S0) {
    return;
  }

  lv_obj_t* scene_0 = lv_obj_create(NULL);
  lv_create_s_0(scene_0);
  lv_screen_load(scene_0);
  activeScene = S0;
}
lv_obj_t* lable_1_1;
String lable_1_1_text = "";
char TB_Text[] = "TB";
char RES_Text[] = "RES";
char STB_Text[] = "STB";

void lv_create_s_1_1(lv_obj_t* parent) {
  //lable
  lable_1_1 = lv_label_create(parent);
  lv_obj_set_width(lable_1_1, lv_pct(50));
  lv_label_set_text(lable_1_1, "Hello World \n grüezi miteinander");

  //TBbutton
  lv_obj_t* TB_bttn = lv_button_create(parent);
  lv_obj_align(TB_bttn, LV_ALIGN_TOP_RIGHT, -10, 10);
  lv_obj_add_event_cb(TB_bttn, btn_1_1_callback, LV_EVENT_CLICKED, TB_Text);


  lv_obj_t* TB_bttn_lable = lv_label_create(TB_bttn);
  lv_label_set_text(TB_bttn_lable, LV_SYMBOL_BACKSPACE);

  //Resing Button
  lv_obj_t* Resing_bttn = lv_button_create(parent);
  lv_obj_align(Resing_bttn, LV_ALIGN_RIGHT_MID, -10, 0);
  lv_obj_add_event_cb(Resing_bttn, btn_1_1_callback, LV_EVENT_CLICKED, RES_Text);


  lv_obj_t* Resing_bttn_lable = lv_label_create(Resing_bttn);
  lv_label_set_text(Resing_bttn_lable, "Aufgeben");

  //Stable button
  lv_obj_t* stable_bttn = lv_button_create(parent);
  lv_obj_align(stable_bttn, LV_ALIGN_BOTTOM_RIGHT, -10, -10);
  lv_obj_add_event_cb(stable_bttn, btn_1_1_callback, LV_EVENT_CLICKED, STB_Text);


  lv_obj_t* stable_bttn_lable = lv_label_create(stable_bttn);
  lv_label_set_text(stable_bttn_lable, "Stabilisieren");
}


void lable_1_1_push(String line) {
  if (lable_1_1_text != "") {
    lable_1_1_text += "\n";
  }
  lable_1_1_text += line;
  lv_label_set_text(lable_1_1, lable_1_1_text.c_str());
}

void lable_1_1_clear() {
  lable_1_1_text = "";
  lv_label_set_text(lable_1_1, lable_1_1_text.c_str());
}

void lable_1_1_rm() {
  int i = lable_1_1_text.lastIndexOf("\n");
  if (i == -1) {
    lable_1_1_clear();
  } else {
    lable_1_1_text.remove(i);
    lv_label_set_text(lable_1_1, lable_1_1_text.c_str());
  }
}


static void btn_1_1_callback(lv_event_t* e) {

  Serial.print("COM:BTN1_1:");
  Serial.println((char*)lv_event_get_user_data(e));
}

#include "S_End.h"

#include <Arduino.h>
#include <lvgl.h>
#include "activeScene.h"

void lv_create_s_end(lv_obj_t* parent, String type);
static void restart_bttn_callback(lv_event_t* e);

//Endscreen


//TODO Brauchen wir diese Funktion?
void lv_create_s_1_2_p(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Patt!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_center(text_label);
}

void transition_s_1_2(String type) {
  if (!((type == "r") || (type == "p") || (type == "w") || (type == "b"))) {
    LV_LOG_WARN("Invalid game outcome. only b,w,r,p are allowed");
    return;
  }


  lv_obj_t* scene_1_2 = lv_obj_create(NULL);

  lv_create_s_end(scene_1_2, type);

  lv_screen_load_anim(scene_1_2, LV_SCR_LOAD_ANIM_MOVE_TOP, 1000, 0, true);
  activeScene = S_End;
}

void lv_create_s_end(lv_obj_t* parent, String type) {
  lv_obj_t* text_label = lv_label_create(parent);

  if (type == "r") {
    lv_label_set_text(text_label, "Remie!");
  } else if (type == "p") {
    lv_label_set_text(text_label, "Patt!");
  } else if (type == "w") {
    lv_label_set_text(text_label, "Sieg fuer Weis!");
  } else if (type == "b") {
    lv_label_set_text(text_label, "Sieg fuer Schwarz!");
  }

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_center(text_label);


  //Restart_button
  lv_obj_t* Restart_bttn = lv_button_create(parent);
  lv_obj_align(Restart_bttn, LV_ALIGN_BOTTOM_MID, 0, -10);
  lv_obj_add_event_cb(Restart_bttn, restart_bttn_callback, LV_EVENT_CLICKED, NULL);


  lv_obj_t* Restart_bttn_lable = lv_label_create(Restart_bttn);
  lv_label_set_text(Restart_bttn_lable, "Neustart");
}

static void restart_bttn_callback(lv_event_t* e) {
  Serial.println("Restart_BTN");
}

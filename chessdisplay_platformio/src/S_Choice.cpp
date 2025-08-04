#include "S_Choice.h"

#include <Arduino.h>
#include <lvgl.h>
#include "activeScene.h"

void lv_create_colurtab(lv_obj_t* parent);
void lv_create_skilltab(lv_obj_t* parent);
static void btn_1_0_callback(lv_event_t* e);

//Choice Scene

void transition_s_Choice() {
  if (activeScene == S_Choice) {
    return;
  }

  lv_obj_t* scene_1_0 = lv_obj_create(NULL);

  lv_obj_t* choicetabs = lv_tabview_create(scene_1_0);

  lv_obj_t* colurtab = lv_tabview_add_tab(choicetabs, "Farbwahl");
  lv_create_colurtab(colurtab);

  lv_obj_t* skilltab = lv_tabview_add_tab(choicetabs, "Schwierigkeit");
  lv_create_skilltab(skilltab);

  lv_screen_load(scene_1_0);
  activeScene = S_Choice;
}

char CB_Text[] = "CB";
char CR_Text[] = "CR";
char CW_Text[] = "CW";

void lv_create_colurtab(lv_obj_t* parent) {

  //Top Text
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Choose your Fighter!");

  lv_obj_set_style_text_align(text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(text_label, LV_ALIGN_TOP_MID, 0, 10);


  //Buttons

  static lv_style_t imgstyle;
  lv_style_init(&imgstyle);
  lv_style_set_width(&imgstyle, 50);
  lv_style_set_height(&imgstyle, 50);


  //Button Black

  lv_obj_t* bk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(bk_btn, btn_1_0_callback, LV_EVENT_CLICKED, CB_Text);
  lv_obj_align(bk_btn, LV_ALIGN_LEFT_MID, 5, 0);

  LV_IMAGE_DECLARE(Black_King);
  lv_obj_t* bkimg = lv_image_create(bk_btn);
  lv_image_set_src(bkimg, &Black_King);
  lv_obj_add_style(bkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(bkimg, 512);

  // Button White

  lv_obj_t* wk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(wk_btn, btn_1_0_callback, LV_EVENT_CLICKED, CW_Text);
  lv_obj_align(wk_btn, LV_ALIGN_RIGHT_MID, -5, 0);

  LV_IMAGE_DECLARE(White_King);
  lv_obj_t* wkimg = lv_image_create(wk_btn);
  lv_image_set_src(wkimg, &White_King);
  lv_obj_add_style(wkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(wkimg, 512);

  // Button Random

  lv_obj_t* wbk_btn = lv_button_create(parent);
  lv_obj_add_event_cb(wbk_btn, btn_1_0_callback, LV_EVENT_CLICKED, CR_Text);
  lv_obj_align(wbk_btn, LV_ALIGN_CENTER, 0, 0);

  LV_IMAGE_DECLARE(wbK_1_0);
  lv_obj_t* wbkimg = lv_image_create(wbk_btn);
  lv_image_set_src(wbkimg, &wbK_1_0);
  lv_obj_add_style(wbkimg, &imgstyle, LV_PART_MAIN);
  lv_image_set_scale(wbkimg, 490);
}

lv_obj_t* skill_roller;

static void btn_1_0_callback(lv_event_t* e) {

  Serial.print("Choice:");
  Serial.print((char*)lv_event_get_user_data(e));
  Serial.print(":");
  Serial.println(lv_roller_get_selected(skill_roller));
}



void lv_create_skilltab(lv_obj_t* parent) {
  // Skill Choice

  // Text

  lv_obj_t* skill_text_label = lv_label_create(parent);

  lv_label_set_text(skill_text_label, "Skill level:");

  lv_obj_set_style_text_align(skill_text_label, LV_TEXT_ALIGN_CENTER, 0);
  lv_obj_set_style_text_font(skill_text_label, &lv_font_montserrat_22, 0);

  lv_obj_align(skill_text_label, LV_ALIGN_LEFT_MID, 10, 0);


  // Roller

  skill_roller = lv_roller_create(parent);

  lv_roller_set_options(skill_roller,
                        "0\n"
                        "1\n"
                        "2\n"
                        "3\n"
                        "4\n"
                        "5\n"
                        "6\n"
                        "7\n"
                        "8\n"
                        "9\n"
                        "10\n"
                        "11\n"
                        "12\n"
                        "13\n"
                        "14\n"
                        "15\n"
                        "16\n"
                        "17\n"
                        "18\n"
                        "19\n"
                        "20",
                        LV_ROLLER_MODE_INFINITE);

  lv_roller_set_visible_row_count(skill_roller, 4);
  lv_roller_set_selected(skill_roller,10,LV_ANIM_OFF);

  lv_obj_align(skill_roller,LV_ALIGN_RIGHT_MID, -15, 0);
}

#include "S_Loading.h"

#include <lvgl.h>
#include "activeScene.h"

void lv_create_s_loading(lv_obj_t* parent) {
  lv_obj_t* text_label = lv_label_create(parent);
  lv_label_set_text(text_label, "Loading Engine");
  lv_obj_set_style_text_font(text_label, &lv_font_montserrat_22, 0);
  lv_obj_align(text_label, LV_ALIGN_LEFT_MID, 10, 0);

  lv_obj_t* spinner = lv_spinner_create(parent);
  lv_obj_set_size(spinner, 100, 100);
  lv_obj_align(spinner, LV_ALIGN_RIGHT_MID, -10, 0);
}

void transition_s_Loading() {
  if (activeScene == S_Loading) {
    return;
  }

  lv_obj_t* scene_loading = lv_obj_create(NULL);
  lv_create_s_loading(scene_loading);
  lv_screen_load(scene_loading);
  activeScene = S_Loading;
}
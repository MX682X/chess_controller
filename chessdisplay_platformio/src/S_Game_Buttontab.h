#ifndef S_GAME_BUTTONTAB_H
#define S_GAME_BUTTONTAB_H
#include <lvgl.h>

void lv_create_buttontab(lv_obj_t* parent) ;

void Game_text_push(String line);
void Game_text_clear();
void Game_text_rm();

#endif
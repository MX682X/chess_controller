#ifndef S_GAME_BOARDTAB_H
#define S_GAME_BOARDTAB_H

#include <lvgl.h>

void lv_create_Boardtab(lv_obj_t* parent);
void set_board_fen(const char* fen);

#endif
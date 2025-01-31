void transition_s_Game() {
  if (activeScene == S_Game) {
    return;
  }

  lv_obj_t* scene_Game = lv_obj_create(NULL);

  lv_obj_t* tabview;
  tabview = lv_tabview_create(scene_Game);
  lv_tabview_set_tab_bar_position(tabview, LV_DIR_LEFT);
  lv_tabview_set_tab_bar_size(tabview, 40);

  lv_obj_t* tab1 = lv_tabview_add_tab(tabview, "Tab 1");
  lv_create_buttontab(tab1);

  lv_obj_t* tab2 = lv_tabview_add_tab(tabview, "Tab 2");
  lv_create_Boardtab(tab2);

  lv_screen_load_anim(scene_Game, LV_SCR_LOAD_ANIM_MOVE_TOP, 1000, 0, true);
  activeScene = S_Game;
}
#ifndef ACTIVESCENE_H
#define ACTIVESCENE_H

enum Scenes { S_Discon,
              S_Choice,
              S_Game,
              S_End,
              S_Loading,
              S_Promotion };

extern Scenes activeScene;

#endif
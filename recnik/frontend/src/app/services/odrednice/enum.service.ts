import { Injectable } from '@angular/core';
import { Gender, StanjeOdrednice, VerbForm, VerbKind, WordType } from '../../models';

@Injectable({
  providedIn: 'root'
})
export class EnumService {
  wordTypes: WordType[];
  entryStates: StanjeOdrednice[];
  genders: Gender[];
  verbKinds: VerbKind[];
  verbForms: VerbForm[];


  constructor() {
    this.genders = [
      { name: 'мушки', id: 1 },
      { name: 'женски', id: 2 },
      { name: 'средњи', id: 3 },
      { name: 'мушки (женски)', id: 4 },
      { name: 'женски (мушки)', id: 5 },
      { name: 'мушки (средњи)', id: 6 },
      { name: 'средњи (мушки)', id: 7 },
      { name: 'женски (средњи)', id: 8 },
      { name: 'средњи (женски)', id: 9 },
      { name: 'мушки / женски', id: 10 },
      { name: 'мушки / средњи', id: 11 },
      { name: 'женски / средњи', id: 12 },
    ];
    this.verbKinds = [
      { name: '---', id: null, def2: false },
      { name: 'прелазни', id: 1, def2: false },
      { name: 'непрелазни', id: 2, def2: false },
      { name: 'повратни', id: 3, def2: false },
      { name: 'прелазни и непрелазни', id: 4, def2: false },
      { name: 'непрелазни и прелазни', id: 5, def2: false },
      { name: '(ce) облик', id: 6, def2: true },
    ];
    this.verbForms = [
      { name: '---', id: null },
      { name: 'свршен', id: 1 },
      { name: 'несвршен', id: 2 },
      { name: 'свршен и несвршен', id: 3 },
      { name: 'несвршен и свршен', id: 4 },
      { name: 'свршен (несвршен)', id: 5 },
      { name: 'несвршен (свршен)', id: 6 },
    ];
    this.entryStates = [
      { id: 1, opis: 'обрада' },
      { id: 2, opis: 'редактура' },
      { id: 3, opis: 'уређивање' },
      { id: 4, opis: 'коначна' },
    ];
    this.wordTypes = [
      { name: 'именица', id: 0 },
      { name: 'глагол', id: 1 },
      { name: 'придев', id: 2 },
      { name: 'прилог', id: 3 },
      { name: 'предлог', id: 4 },
      { name: 'заменица', id: 5 },
      { name: 'узвик', id: 6 },
      { name: 'речца', id: 7 },
      { name: 'везник', id: 8 },
      { name: 'број', id: 9 },
      { name: 'остало', id: 10 },
    ];
  }

  getAllGenders(): Gender[] {
    return this.genders;
  }

  getAllVerbKinds(): VerbKind[] {
    return this.verbKinds;
  }

  getAllVerbForms(): VerbForm[] {
    return this.verbForms;
  }

  getAllEntryStates(): StanjeOdrednice[] {
    return this.entryStates;
  }

  getAllWordTypes(): WordType[] {
    return this.wordTypes;
  }

  getGender(id: number): Gender {
    return this.genders[id - 1];
  }

  getVerbKind(id: number): VerbKind {
    return this.verbKinds[id];
  }

  getVerbForm(id: number): VerbForm {
    return this.verbForms[id];
  }

  getEntryState(id: number): StanjeOdrednice {
    return this.entryStates[id - 1];
  }

  getWordType(id: number): WordType {
    return this.wordTypes[id];
  }
}

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
    ];
    this.verbKinds = [
      { name: 'прелазни', id: 1, def2: false },
      { name: 'непрелазни', id: 2, def2: false },
      { name: 'повратни', id: 3, def2: false },
      { name: 'прелазни + повратни', id: 4, def2: true },
      { name: 'непрелазни + повратни', id: 5, def2: true },
    ];
    this.verbForms = [
      { name: 'свршен', id: 1 },
      { name: 'несвршен', id: 2 },
      { name: 'двовидски', id: 3 },
    ];
    this.entryStates = [
      { id: 1, opis: 'почетна обрада' },
      { id: 2, opis: 'редактура 1' },
      { id: 3, opis: 'редактура 2' },
      { id: 4, opis: 'коначан запис' },
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
    return this.verbKinds[id - 1];
  }

  getVerbForm(id: number): VerbForm {
    return this.verbForms[id - 1];
  }

  getEntryState(id: number): StanjeOdrednice {
    return this.entryStates[id - 1];
  }

  getWordType(id: number): WordType {
    return this.wordTypes[id];
  }
}

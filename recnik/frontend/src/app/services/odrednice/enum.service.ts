import { Injectable } from '@angular/core';
import { Gender, VerbForm, VerbKind } from '../../models';

@Injectable({
  providedIn: 'root'
})
export class EnumService {
  genders: Gender[];
  verbKinds: VerbKind[];
  verbForms: VerbForm[];

  constructor() {
    this.genders = [
      { name: 'Мушки', id: 1 },
      { name: 'Женски', id: 2 },
      { name: 'Средњи', id: 3 },
    ];
    this.verbKinds = [
      { name: 'Прелазни', id: 1 },
      { name: 'Непрелазни', id: 2 },
      { name: 'Повратни', id: 3 },
      { name: 'Узајамно повратни', id: 4 },
    ];
    this.verbForms = [
      { name: 'Свршен', id: 1 },
      { name: 'Несвршен', id: 2 },
      { name: 'Двовидски', id: 3 },
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

  getGender(id: number): Gender {
    return this.genders[id - 1];
  }

  getVerbKind(id: number): VerbKind {
    return this.verbKinds[id - 1];
  }

  getVerbForm(id: number): VerbForm {
    return this.verbForms[id - 1];
  }
}

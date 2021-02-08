export interface Gender {
  name: string;
  id: number;
}

export interface VerbKind {
  name: string;
  id: number;
}

export interface VerbForm {
  name: string;
  id: number;
}

export interface StanjeOdrednice {
  id: number;
  opis: string;
}

export const STANJE_ODREDNICE: StanjeOdrednice[] = [
  { id: 1, opis: 'Почетна обрада' },
  { id: 2, opis: 'Редактура 1' },
  { id: 3, opis: 'Редактура 2' },
  { id: 4, opis: 'Коначан запис' },
];

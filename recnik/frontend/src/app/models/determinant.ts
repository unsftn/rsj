export interface Determinant {
  id?: number;
  rec: string;
  varijante: any[];
  ijekavski?: string;
  vrsta: number;
  rod?: number;
  nastavak?: string;
  info?: string;
  glagolski_vid?: number;
  glagolski_rod?: number;
  prezent?: string;
  stanje: number;
  version: number;
  opciono_se?: boolean;
  kolokacija_set?: any[];
  kvalifikatori: any[];
  znacenja: any[];
  izrazi_fraze: any[];
}

export interface Determinant {
  id?: number;
  rec: string;
  varijante: any[];
  ijekavski?: string;
  vrsta: number;
  rod?: number;
  nastavak?: string;
  nastavak_ij?: string;
  info?: string;
  glagolski_vid?: number;
  glagolski_rod?: number;
  prezent?: string;
  prezent_ij?: string;
  stanje: number;
  version: number;
  opciono_se?: boolean;
  rbr_homonima?: number;
  napomene: string;
  freetext: string;
  kvalifikatori: any[];
  znacenja: any[];
  izrazi_fraze: any[];
  sinonimi: any[];
  antonimi: any[];
  kolokacije: any[];
}

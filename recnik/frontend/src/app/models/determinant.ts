export interface Determinant {
  id?: number;
  rec: string;
  varijante: any[];
  ijekavski?: string;
  vrsta: number;
  podvrsta_id?: number;
  rod?: number;
  nastavak?: string;
  nastavak_ij?: string;
  info?: string;
  glagolski_vid?: number;
  glagolski_rod?: number;
  prikazi_gl_rod?: boolean;
  ima_se_znacenja?: boolean;
  prezent?: string;
  prezent_ij?: string;
  stanje: number;
  version: number;
  opciono_se?: boolean;
  rbr_homonima?: number;
  status_id?: number;
  napomene: string;
  freetext: string;
  kvalifikatori: any[];
  znacenja: any[];
  izrazi_fraze: any[];
  // sinonimi: any[];
  // antonimi: any[];
  kolokacije: any[];
  ravnopravne_varijante: boolean;
}

export interface DeterminantStatus {
  id: number;
  naziv: string;
}

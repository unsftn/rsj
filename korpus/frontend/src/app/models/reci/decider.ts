export interface GenerisaniSpisak {
  id: number;
  start_time: Date;
  end_time: Date;
}

export interface RecZaOdluku {
  id: number;
  prvo_slovo: string;
  tekst: string;
  vrsta_reci: number;
  korpus_id: number;
  recnik_id: number;
  odluka: number;
  broj_publikacija: number;
  broj_pojavljivanja: number;
  poslednje_generisanje: number;
  vreme_odluke: Date;
  donosilac_odluke: number;
  beleska: string;
}

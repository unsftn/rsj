export interface Imenica {
  id?: number;
  vrsta?: number;
  recnikID?: number;
  redni_broj?: number;
  nomjed: string;
  genjed: string;
  datjed: string;
  akujed: string;
  vokjed: string;
  insjed: string;
  lokjed: string;
  nommno: string;
  genmno: string;
  datmno: string;
  akumno: string;
  vokmno: string;
  insmno: string;
  lokmno: string;
  izmene?: any[];
  varijante?: Imenica[];
}

export function toImenica(obj: any): Imenica {
  return {
    id: obj.id,
    vrsta: obj.vrsta,
    recnikID: obj.recnik_id,
    nomjed: obj.nomjed,
    genjed: obj.genjed,
    datjed: obj.datjed,
    akujed: obj.akujed,
    vokjed: obj.vokjed,
    insjed: obj.insjed,
    lokjed: obj.lokjed,
    nommno: obj.nommno,
    genmno: obj.genmno,
    datmno: obj.datmno,
    akumno: obj.akumno,
    vokmno: obj.vokmno,
    insmno: obj.insmno,
    lokmno: obj.lokmno,
    izmene: obj.izmenaimenice_set,
    varijante: obj.varijantaimenice_set.map((item) => ({
      redni_broj: item.redni_broj,
      nomjed: item.nomjed,
      genjed: item.genjed,
      datjed: item.datjed,
      akujed: item.akujed,
      vokjed: item.vokjed,
      insjed: item.insjed,
      lokjed: item.lokjed,
      nommno: item.nommno,
      genmno: item.genmno,
      datmno: item.datmno,
      akumno: item.akumno,
      vokmno: item.vokmno,
      insmno: item.insmno,
      lokmno: item.lokmno})).sort((a, b) => a.rbr - b.rbr)
  };
}

export interface VrstaImenice {
  id: number;
  name: string;
}

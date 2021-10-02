export interface VrstaImenice {
  id: number;
  name: string;
}

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

export interface GlagolskiRod {
  id: number;
  name: string;
}

export interface GlagolskiVid {
  id: number;
  name: string;
}

export interface VarijantaGlagola {
  varijanta: number;
  tekst: string;
}

export interface OblikGlagola {
  vreme: number;
  jd1: string;
  jd2: string;
  jd3: string;
  mn1: string;
  mn2: string;
  mn3: string;
  varijante: VarijantaGlagola[];
}

export interface Glagol {
  id?: number;
  gl_rod: number;
  gl_vid: number;
  infinitiv: string;
  rgp_mj: string;
  rgp_zj: string;
  rgp_sj: string;
  rgp_mm: string;
  rgp_zm: string;
  rgp_sm: string;
  gpp: string;
  gps: string;
  recnikID?: number;
  izmene?: any;
  oblici: OblikGlagola[];
}

export function toGlagol(obj: any): Glagol {
  return {
    id: obj.id,
    gl_rod: obj.gl_rod,
    gl_vid: obj.gl_vid,
    infinitiv: obj.infinitiv,
    recnikID: obj.recnik_id,
    rgp_mj: obj.rgp_mj,
    rgp_zj: obj.rgp_zj,
    rgp_sj: obj.rgp_sj,
    rgp_mm: obj.rgp_mm,
    rgp_zm: obj.rgp_zm,
    rgp_sm: obj.rgp_sm,
    gpp: obj.gpp,
    gps: obj.gps,
    izmene: obj.izmenaglagola_set,
    oblici: obj.oblikglagola_set.map((oblik) => ({
      vreme: oblik.vreme,
      jd1: oblik.jd1,
      jd2: oblik.jd2,
      jd3: oblik.jd3,
      mn1: oblik.mn1,
      mn2: oblik.mn2,
      mn3: oblik.mn3,
      varijante: oblik.varijanteglagola_set.map((v) => ({
        varijanta: v.varijanta,
        tekst: v.tekst
      }))
    }))
  };
}
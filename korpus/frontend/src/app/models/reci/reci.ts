function nvl(x: string): string { 
  if (x === null || x === undefined) return '';
  return x;
}

function nvlObj(obj: any): any {
  for (const propName of Object.getOwnPropertyNames(obj)) {
    obj[propName] = nvl(obj[propName]);
  }
  return obj;
}

export interface VrstaImenice {
  id: number;
  name: string;
}

export interface Imenica {
  id?: number;
  vrsta?: number;
  recnikID?: number;
  vlasnikID?: number;
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
    vlasnikID: obj.vlasnik,
    nomjed: nvl(obj.nomjed),
    genjed: nvl(obj.genjed),
    datjed: nvl(obj.datjed),
    akujed: nvl(obj.akujed),
    vokjed: nvl(obj.vokjed),
    insjed: nvl(obj.insjed),
    lokjed: nvl(obj.lokjed),
    nommno: nvl(obj.nommno),
    genmno: nvl(obj.genmno),
    datmno: nvl(obj.datmno),
    akumno: nvl(obj.akumno),
    vokmno: nvl(obj.vokmno),
    insmno: nvl(obj.insmno),
    lokmno: nvl(obj.lokmno),
    izmene: obj.izmenaimenice_set,
    varijante: obj.varijantaimenice_set.map((item) => ({
      redni_broj: item.redni_broj,
      nomjed: nvl(item.nomjed),
      genjed: nvl(item.genjed),
      datjed: nvl(item.datjed),
      akujed: nvl(item.akujed),
      vokjed: nvl(item.vokjed),
      insjed: nvl(item.insjed),
      lokjed: nvl(item.lokjed),
      nommno: nvl(item.nommno),
      genmno: nvl(item.genmno),
      datmno: nvl(item.datmno),
      akumno: nvl(item.akumno),
      vokmno: nvl(item.vokmno),
      insmno: nvl(item.insmno),
      lokmno: nvl(item.lokmno)})).sort((a, b) => a.rbr - b.rbr)
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

export interface GlagolskaVarijanta {
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
  vlasnikID?: number;
  izmene?: any;
  oblici: OblikGlagola[];
}

export function toGlagol(obj: any): Glagol {
  const glagol = {
    id: obj.id,
    gl_rod: obj.gl_rod,
    gl_vid: obj.gl_vid,
    infinitiv: nvl(obj.infinitiv),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
    rgp_mj: nvl(obj.rgp_mj),
    rgp_zj: nvl(obj.rgp_zj),
    rgp_sj: nvl(obj.rgp_sj),
    rgp_mm: nvl(obj.rgp_mm),
    rgp_zm: nvl(obj.rgp_zm),
    rgp_sm: nvl(obj.rgp_sm),
    gpp: nvl(obj.gpp),
    gps: nvl(obj.gps),
    izmene: obj.izmenaglagola_set,
    oblici: Array(5).fill({vreme: 0, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: []}),
  };
  for (const o of obj.oblikglagola_set) {
    glagol.oblici[o.vreme - 1] = {
      vreme: o.vreme,
      jd1: nvl(o.jd1),
      jd2: nvl(o.jd2),
      jd3: nvl(o.jd3),
      mn1: nvl(o.mn1),
      mn2: nvl(o.mn2),
      mn3: nvl(o.mn3),
      varijante: o.varijanteglagola_set.map((v) => ({
        varijanta: v.varijanta,
        tekst: nvl(v.tekst)
      }))
    }
  }
  for (let i = 0; i < 5; i++) {
    if (glagol.oblici[i].vreme === 0)
      glagol.oblici[i].vreme = i + 1;
  }
  return glagol;
}

export interface PridevskiVid {
  id: number;
  name: string;
}

export interface VidPrideva {
  vid: number;
  mnomjed: string;
  mgenjed: string;
  mdatjed: string;
  makujed: string;
  mvokjed: string;
  minsjed: string;
  mlokjed: string;
  mnommno: string;
  mgenmno: string;
  mdatmno: string;
  makumno: string;
  mvokmno: string;
  minsmno: string;
  mlokmno: string;
  znomjed: string;
  zgenjed: string;
  zdatjed: string;
  zakujed: string;
  zvokjed: string;
  zinsjed: string;
  zlokjed: string;
  znommno: string;
  zgenmno: string;
  zdatmno: string;
  zakumno: string;
  zvokmno: string;
  zinsmno: string;
  zlokmno: string;
  snomjed: string;
  sgenjed: string;
  sdatjed: string;
  sakujed: string;
  svokjed: string;
  sinsjed: string;
  slokjed: string;
  snommno: string;
  sgenmno: string;
  sdatmno: string;
  sakumno: string;
  svokmno: string;
  sinsmno: string;
  slokmno: string;
}

export interface Pridev {
  id?: number;
  dvaVida?: boolean;
  vidovi: VidPrideva[];
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any;
}

function getVid(vidovi: VidPrideva[], vid: number): VidPrideva {
  let v = vidovi.filter(v => v.vid == vid);
  if (v.length > 0)
    return nvlObj(v[0]);
  else
    return {
      vid: vid,
      mnomjed: '',
      mgenjed: '',
      mdatjed: '',
      makujed: '',
      mvokjed: '',
      minsjed: '',
      mlokjed: '',
      mnommno: '',
      mgenmno: '',
      mdatmno: '',
      makumno: '',
      mvokmno: '',
      minsmno: '',
      mlokmno: '',
      znomjed: '',
      zgenjed: '',
      zdatjed: '',
      zakujed: '',
      zvokjed: '',
      zinsjed: '',
      zlokjed: '',
      znommno: '',
      zgenmno: '',
      zdatmno: '',
      zakumno: '',
      zvokmno: '',
      zinsmno: '',
      zlokmno: '',
      snomjed: '',
      sgenjed: '',
      sdatjed: '',
      sakujed: '',
      svokjed: '',
      sinsjed: '',
      slokjed: '',
      snommno: '',
      sgenmno: '',
      sdatmno: '',
      sakumno: '',
      svokmno: '',
      sinsmno: '',
      slokmno: ''
    }
}

export function toPridev(obj: any): Pridev {
  const vidovi: VidPrideva[] = [];
  vidovi.push(getVid(obj.vidprideva_set, 1));
  vidovi.push(getVid(obj.vidprideva_set, 2));
  vidovi.push(getVid(obj.vidprideva_set, 3));
  vidovi.push(getVid(obj.vidprideva_set, 4));
  return {
    id: obj.id,
    dvaVida: obj.dva_vida,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
    izmene: obj.izmenaprideva_set,
    vidovi: vidovi    
  };
}

export interface Predlog {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any;
}

export function toPredlog(obj: any): Predlog {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
  };
}

export interface Uzvik {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any;
}

export function toUzvik(obj: any): Uzvik {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
  };
}

export interface Recca {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any;
}

export function toRecca(obj: any): Recca {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
  };
}

export interface Veznik {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any;
}

export function toVeznik(obj: any): Veznik {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
  };
}

export interface Zamenica {
  id?: number;
  redni_broj?: number;
  nomjed: string;
  genjed: string;
  datjed: string;
  akujed: string;
  vokjed: string;
  insjed: string;
  lokjed: string;
  recnikID?: number;
  vlasnikID?: number;
  izmene?: any[];
  varijante?: Zamenica[];
}

export function toZamenica(obj: any): Zamenica {
  return {
    id: obj.id,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
    nomjed: nvl(obj.nomjed),
    genjed: nvl(obj.genjed),
    datjed: nvl(obj.datjed),
    akujed: nvl(obj.akujed),
    vokjed: nvl(obj.vokjed),
    insjed: nvl(obj.insjed),
    lokjed: nvl(obj.lokjed),
    varijante: obj.varijantazamenice_set.map((item) => ({
      redni_broj: item.redni_broj,
      nomjed: nvl(item.nomjed),
      genjed: nvl(item.genjed),
      datjed: nvl(item.datjed),
      akujed: nvl(item.akujed),
      vokjed: nvl(item.vokjed),
      insjed: nvl(item.insjed),
      lokjed: nvl(item.lokjed)})).sort((a, b) => a.rbr - b.rbr)
  };
}

export interface Broj {
  id?: number;
  recnikID?: number;
  vlasnikID?: number;
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
}

export function toBroj(obj: any): Broj {
  return {
    id: obj.id,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
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
    lokmno: obj.lokmno
  };
}

export interface Prilog {
  id?: number;
  recnikID?: number;
  vlasnikID?: number;
  komparativ: string;
  superlativ: string;
  izmene?: any[];
}

export function toPrilog(obj: any): Prilog {
  return {
    id: obj.id,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik,
    komparativ: obj.komparativ,
    superlativ: obj.superlativ,
  };
}


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
  izmene?: any;
  oblici: OblikGlagola[];
}

export function toGlagol(obj: any): Glagol {
  const glagol = {
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
    oblici: Array(5).fill({vreme: 0, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: []}),
  };
  for (const o of obj.oblikglagola_set) {
    glagol.oblici[o.vreme - 1] = {
      vreme: o.vreme,
      jd1: o.jd1,
      jd2: o.jd2,
      jd3: o.jd3,
      mn1: o.mn1,
      mn2: o.mn2,
      mn3: o.mn3,
      varijante: o.varijanteglagola_set.map((v) => ({
        varijanta: v.varijanta,
        tekst: v.tekst
      }))
    }
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
  vidovi: VidPrideva[];
  recnikID?: number;
  izmene?: any;
}

function getVid(vidovi: VidPrideva[], vid: number): VidPrideva {
  let v = vidovi.filter(v => v.vid == vid);
  if (v.length > 0)
    return v[0];
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
    recnikID: obj.recnik_id,
    izmene: obj.izmenaprideva_set,
    vidovi: vidovi    
  };
}

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
  vlasnik?: any;
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
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
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
  gpp2: string;
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
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
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
    rgp_mj: nvl(obj.rgp_mj),
    rgp_zj: nvl(obj.rgp_zj),
    rgp_sj: nvl(obj.rgp_sj),
    rgp_mm: nvl(obj.rgp_mm),
    rgp_zm: nvl(obj.rgp_zm),
    rgp_sm: nvl(obj.rgp_sm),
    gpp: nvl(obj.gpp),
    gps: nvl(obj.gps),
    gpp2: nvl(obj.gpp2),
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

export interface VarijantaPrideva {
  rod: number;
  redni_broj: number;
  onomjed: string;
  ogenjed: string;
  odatjed: string;
  oakujed: string;
  ovokjed: string;
  oinsjed: string;
  olokjed: string;
  nnomjed: string;
  ngenjed: string;
  ndatjed: string;
  nakujed: string;
  nvokjed: string;
  ninsjed: string;
  nlokjed: string;
  pnomjed: string;
  pgenjed: string;
  pdatjed: string;
  pakujed: string;
  pvokjed: string;
  pinsjed: string;
  plokjed: string;
  knomjed: string;
  kgenjed: string;
  kdatjed: string;
  kakujed: string;
  kvokjed: string;
  kinsjed: string;
  klokjed: string;
  snomjed: string;
  sgenjed: string;
  sdatjed: string;
  sakujed: string;
  svokjed: string;
  sinsjed: string;
  slokjed: string;
}

export interface Pridev {
  id?: number;
  dvaVida?: boolean;
  varijante: VarijantaPrideva[];
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
  izmene?: any;
  monomjed: string;
  mogenjed: string;
  modatjed: string;
  moakujed: string;
  movokjed: string;
  moinsjed: string;
  molokjed: string;
  monommno: string;
  mogenmno: string;
  modatmno: string;
  moakumno: string;
  movokmno: string;
  moinsmno: string;
  molokmno: string;
  mnnomjed: string;
  mngenjed: string;
  mndatjed: string;
  mnakujed: string;
  mnvokjed: string;
  mninsjed: string;
  mnlokjed: string;
  mnnommno: string;
  mngenmno: string;
  mndatmno: string;
  mnakumno: string;
  mnvokmno: string;
  mninsmno: string;
  mnlokmno: string;
  mknomjed: string;
  mkgenjed: string;
  mkdatjed: string;
  mkakujed: string;
  mkvokjed: string;
  mkinsjed: string;
  mklokjed: string;
  mknommno: string;
  mkgenmno: string;
  mkdatmno: string;
  mkakumno: string;
  mkvokmno: string;
  mkinsmno: string;
  mklokmno: string;
  msnomjed: string;
  msgenjed: string;
  msdatjed: string;
  msakujed: string;
  msvokjed: string;
  msinsjed: string;
  mslokjed: string;
  msnommno: string;
  msgenmno: string;
  msdatmno: string;
  msakumno: string;
  msvokmno: string;
  msinsmno: string;
  mslokmno: string;
  zpnomjed: string;
  zpgenjed: string;
  zpdatjed: string;
  zpakujed: string;
  zpvokjed: string;
  zpinsjed: string;
  zplokjed: string;
  zpnommno: string;
  zpgenmno: string;
  zpdatmno: string;
  zpakumno: string;
  zpvokmno: string;
  zpinsmno: string;
  zplokmno: string;
  zknomjed: string;
  zkgenjed: string;
  zkdatjed: string;
  zkakujed: string;
  zkvokjed: string;
  zkinsjed: string;
  zklokjed: string;
  zknommno: string;
  zkgenmno: string;
  zkdatmno: string;
  zkakumno: string;
  zkvokmno: string;
  zkinsmno: string;
  zklokmno: string;
  zsnomjed: string;
  zsgenjed: string;
  zsdatjed: string;
  zsakujed: string;
  zsvokjed: string;
  zsinsjed: string;
  zslokjed: string;
  zsnommno: string;
  zsgenmno: string;
  zsdatmno: string;
  zsakumno: string;
  zsvokmno: string;
  zsinsmno: string;
  zslokmno: string;
  spnomjed: string;
  spgenjed: string;
  spdatjed: string;
  spakujed: string;
  spvokjed: string;
  spinsjed: string;
  splokjed: string;
  spnommno: string;
  spgenmno: string;
  spdatmno: string;
  spakumno: string;
  spvokmno: string;
  spinsmno: string;
  splokmno: string;
  sknomjed: string;
  skgenjed: string;
  skdatjed: string;
  skakujed: string;
  skvokjed: string;
  skinsjed: string;
  sklokjed: string;
  sknommno: string;
  skgenmno: string;
  skdatmno: string;
  skakumno: string;
  skvokmno: string;
  skinsmno: string;
  sklokmno: string;
  ssnomjed: string;
  ssgenjed: string;
  ssdatjed: string;
  ssakujed: string;
  ssvokjed: string;
  ssinsjed: string;
  sslokjed: string;
  ssnommno: string;
  ssgenmno: string;
  ssdatmno: string;
  ssakumno: string;
  ssvokmno: string;
  ssinsmno: string;
  sslokmno: string;
}

function getVarijanta(pridev: Pridev, rod: number, redni_broj: number): VarijantaPrideva {
  let varijante = pridev.varijante.filter(v => v.rod === rod && v.redni_broj === redni_broj);
  if (varijante.length > 0)
    return nvlObj(varijante[0]);
  else
    return {
      rod: rod,
      redni_broj: redni_broj,
      onomjed: '',
      ogenjed: '',
      odatjed: '',
      oakujed: '',
      ovokjed: '',
      oinsjed: '',
      olokjed: '',
      nnomjed: '',
      ngenjed: '',
      ndatjed: '',
      nakujed: '',
      nvokjed: '',
      ninsjed: '',
      nlokjed: '',
      pnomjed: '',
      pgenjed: '',
      pdatjed: '',
      pakujed: '',
      pvokjed: '',
      pinsjed: '',
      plokjed: '',
      knomjed: '',
      kgenjed: '',
      kdatjed: '',
      kakujed: '',
      kvokjed: '',
      kinsjed: '',
      klokjed: '',
      snomjed: '',
      sgenjed: '',
      sdatjed: '',
      sakujed: '',
      svokjed: '',
      sinsjed: '',
      slokjed: '',
    }
}

export function toPridev(obj: any): Pridev {
  return {
    id: obj.id,
    dvaVida: obj.dva_vida,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
    varijante: obj.varijantaprideva_set,
    izmene: obj.izmenaprideva_set,
    monomjed: obj.monomjed,
    mogenjed: obj.mogenjed,
    modatjed: obj.modatjed,
    moakujed: obj.moakujed,
    movokjed: obj.movokjed,
    moinsjed: obj.moinsjed,
    molokjed: obj.molokjed,
    monommno: obj.monommno,
    mogenmno: obj.mogenmno,
    modatmno: obj.modatmno,
    moakumno: obj.moakumno,
    movokmno: obj.movokmno,
    moinsmno: obj.moinsmno,
    molokmno: obj.molokmno,
    mnnomjed: obj.mnnomjed,
    mngenjed: obj.mngenjed,
    mndatjed: obj.mndatjed,
    mnakujed: obj.mnakujed,
    mnvokjed: obj.mnvokjed,
    mninsjed: obj.mninsjed,
    mnlokjed: obj.mnlokjed,
    mnnommno: obj.mnnommno,
    mngenmno: obj.mngenmno,
    mndatmno: obj.mndatmno,
    mnakumno: obj.mnakumno,
    mnvokmno: obj.mnvokmno,
    mninsmno: obj.mninsmno,
    mnlokmno: obj.mnlokmno,
    mknomjed: obj.mknomjed,
    mkgenjed: obj.mkgenjed,
    mkdatjed: obj.mkdatjed,
    mkakujed: obj.mkakujed,
    mkvokjed: obj.mkvokjed,
    mkinsjed: obj.mkinsjed,
    mklokjed: obj.mklokjed,
    mknommno: obj.mknommno,
    mkgenmno: obj.mkgenmno,
    mkdatmno: obj.mkdatmno,
    mkakumno: obj.mkakumno,
    mkvokmno: obj.mkvokmno,
    mkinsmno: obj.mkinsmno,
    mklokmno: obj.mklokmno,
    msnomjed: obj.msnomjed,
    msgenjed: obj.msgenjed,
    msdatjed: obj.msdatjed,
    msakujed: obj.msakujed,
    msvokjed: obj.msvokjed,
    msinsjed: obj.msinsjed,
    mslokjed: obj.mslokjed,
    msnommno: obj.msnommno,
    msgenmno: obj.msgenmno,
    msdatmno: obj.msdatmno,
    msakumno: obj.msakumno,
    msvokmno: obj.msvokmno,
    msinsmno: obj.msinsmno,
    mslokmno: obj.mslokmno,
    zpnomjed: obj.zpnomjed,
    zpgenjed: obj.zpgenjed,
    zpdatjed: obj.zpdatjed,
    zpakujed: obj.zpakujed,
    zpvokjed: obj.zpvokjed,
    zpinsjed: obj.zpinsjed,
    zplokjed: obj.zplokjed,
    zpnommno: obj.zpnommno,
    zpgenmno: obj.zpgenmno,
    zpdatmno: obj.zpdatmno,
    zpakumno: obj.zpakumno,
    zpvokmno: obj.zpvokmno,
    zpinsmno: obj.zpinsmno,
    zplokmno: obj.zplokmno,
    zknomjed: obj.zknomjed,
    zkgenjed: obj.zkgenjed,
    zkdatjed: obj.zkdatjed,
    zkakujed: obj.zkakujed,
    zkvokjed: obj.zkvokjed,
    zkinsjed: obj.zkinsjed,
    zklokjed: obj.zklokjed,
    zknommno: obj.zknommno,
    zkgenmno: obj.zkgenmno,
    zkdatmno: obj.zkdatmno,
    zkakumno: obj.zkakumno,
    zkvokmno: obj.zkvokmno,
    zkinsmno: obj.zkinsmno,
    zklokmno: obj.zklokmno,
    zsnomjed: obj.zsnomjed,
    zsgenjed: obj.zsgenjed,
    zsdatjed: obj.zsdatjed,
    zsakujed: obj.zsakujed,
    zsvokjed: obj.zsvokjed,
    zsinsjed: obj.zsinsjed,
    zslokjed: obj.zslokjed,
    zsnommno: obj.zsnommno,
    zsgenmno: obj.zsgenmno,
    zsdatmno: obj.zsdatmno,
    zsakumno: obj.zsakumno,
    zsvokmno: obj.zsvokmno,
    zsinsmno: obj.zsinsmno,
    zslokmno: obj.zslokmno,
    spnomjed: obj.spnomjed,
    spgenjed: obj.spgenjed,
    spdatjed: obj.spdatjed,
    spakujed: obj.spakujed,
    spvokjed: obj.spvokjed,
    spinsjed: obj.spinsjed,
    splokjed: obj.splokjed,
    spnommno: obj.spnommno,
    spgenmno: obj.spgenmno,
    spdatmno: obj.spdatmno,
    spakumno: obj.spakumno,
    spvokmno: obj.spvokmno,
    spinsmno: obj.spinsmno,
    splokmno: obj.splokmno,
    sknomjed: obj.sknomjed,
    skgenjed: obj.skgenjed,
    skdatjed: obj.skdatjed,
    skakujed: obj.skakujed,
    skvokjed: obj.skvokjed,
    skinsjed: obj.skinsjed,
    sklokjed: obj.sklokjed,
    sknommno: obj.sknommno,
    skgenmno: obj.skgenmno,
    skdatmno: obj.skdatmno,
    skakumno: obj.skakumno,
    skvokmno: obj.skvokmno,
    skinsmno: obj.skinsmno,
    sklokmno: obj.sklokmno,
    ssnomjed: obj.ssnomjed,
    ssgenjed: obj.ssgenjed,
    ssdatjed: obj.ssdatjed,
    ssakujed: obj.ssakujed,
    ssvokjed: obj.ssvokjed,
    ssinsjed: obj.ssinsjed,
    sslokjed: obj.sslokjed,
    ssnommno: obj.ssnommno,
    ssgenmno: obj.ssgenmno,
    ssdatmno: obj.ssdatmno,
    ssakumno: obj.ssakumno,
    ssvokmno: obj.ssvokmno,
    ssinsmno: obj.ssinsmno,
    sslokmno: obj.sslokmno,
  };
}

export interface Predlog {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
  izmene?: any;
}

export function toPredlog(obj: any): Predlog {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
  };
}

export interface Uzvik {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
  izmene?: any;
}

export function toUzvik(obj: any): Uzvik {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
  };
}

export interface Recca {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
  izmene?: any;
}

export function toRecca(obj: any): Recca {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
  };
}

export interface Veznik {
  id?: number;
  tekst: string;
  recnikID?: number;
  vlasnikID?: number;
  vlasnik?: any;
  izmene?: any;
}

export function toVeznik(obj: any): Veznik {
  return { 
    id: obj.id, 
    tekst: nvl(obj.tekst),
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
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
  vlasnik?: any;
  izmene?: any[];
  varijante?: Zamenica[];
}

export function toZamenica(obj: any): Zamenica {
  return {
    id: obj.id,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
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
  vlasnik?: any;
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
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
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
  vlasnik?: any;
  pozitiv: string;
  komparativ: string;
  superlativ: string;
  izmene?: any[];
}

export function toPrilog(obj: any): Prilog {
  return {
    id: obj.id,
    recnikID: obj.recnik_id,
    vlasnikID: obj.vlasnik.id,
    vlasnik: obj.vlasnik,
    pozitiv: obj.pozitiv,
    komparativ: obj.komparativ,
    superlativ: obj.superlativ,
  };
}


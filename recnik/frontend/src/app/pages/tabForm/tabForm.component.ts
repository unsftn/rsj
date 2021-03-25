import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { MenuItem, PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { Gender, StanjeOdrednice, Determinant, Qualificator, VerbKind, VerbForm, WordType } from '../../models';
import { OdrednicaService, PreviewService, QualificatorService, EnumService } from '../../services/odrednice';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import * as primeri from '../../examples';

interface Variant {
  nameE: string;
  nameI: string;
  extensionE: string;
  extensionI: string;
}

@Component({
  selector: 'app-tab-form',
  templateUrl: './tabForm.component.html',
  styleUrls: ['./tabForm.component.scss'],
})
export class TabFormComponent implements OnInit {
  wordTypes: WordType[];
  isNoun: boolean;
  isVerb: boolean;
  wordE: string;
  wordI: string;
  selectedGender: Gender;
  extensionE: string;
  extensionI: string;
  variants: Variant[];

  genders: Gender[];
  verbKinds: VerbKind[];
  verbForms: VerbForm[];

  selectedVerbKind: VerbKind;
  selectedVerbForm: VerbForm;
  presentE: string;
  presentI: string;
  details: string;

  selectedWordType: WordType;
  selectedState: StanjeOdrednice;
  qualificators: Qualificator[] = [];
  id: number;
  editMode: boolean; // false: nova odrednica; true: edit postojece
  version = 1;
  optionalSe: boolean;
  homonim?: number;

  meanings: any[] = [];
  meanings2: any[] = [];
  expressions: any[] = [];
  collocations: any[] = [];
  synonyms: any[] = [];
  antonyms: any[] = [];

  errorMsg: string;
  showInfoDialog = false;
  showWarningDialog = false;
  showWaitDialog = false;
  showAccentDialog = false;
  baseChar = 'а';
  accentCaretPos = 0;
  accentModelName: string;
  accentTarget: HTMLInputElement;
  accentIndex = -1;
  message: SafeHtml;
  nextRoute: any[];

  undoStack: any[] = [];
  redoStack: any[] = [];
  currentState: any = null;
  dirty: boolean;
  yesHandler: () => void;

  primeri: MenuItem[] = [{
      label: 'ски̏нути',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_1),
    }, {
      label: 'а (узвик)',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_2),
    }, {
      label: 'али',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_3),
    }, {
      label: 'ски̏јати (се)',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_4),
    }, {
      label: 'скло̀нити',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_5),
    }, {
      label: 'сѐдети',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_6),
    }, {
      label: 'ра̑днӣк',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_7),
    }, {
      label: 'мѐњати',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_8),
    }, {
      label: 'мле́ко',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_9),
    }, {
      label: 'ве̏ра',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_10),
    }, {
      label: 'дѐте',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_11),
    }, {
      label: 'ре̑ч',
      command: (event) => this.fillTestOdrednica(primeri.ODREDNICA_12),
    }
  ];

  workflowItems: MenuItem[];
  wfObradjivac: MenuItem[] = [{
      label: 'Проследи редактору',
      command: (event) => this.toRedaktor(),
  }];
  wfRedaktor: MenuItem[] = [{
      label: 'Врати на обраду',
      command: (event) => this.toObradjivac(),
    },{
      label: 'Проследи уреднику',
      command: (event) => this.toUrednik(),
  }];
  wfUrednik: MenuItem[] = [{
      label: 'Врати на обраду',
      command: (event) => this.toObradjivac(),
    },{
      label: 'Врати редактору',
      command: (event) => this.toRedaktor(),
    },{
      label: 'Затвори одредницу',
      command: (event) => this.toKraj(),
  }];
  wfAdministrator: MenuItem[] = [{
      label: 'Врати на обраду',
      command: (event) => this.toObradjivac(),
    },{
      label: 'Врати редактору',
      command: (event) => this.toRedaktor(),
    },{
      label: 'Врати уреднику',
      command: (event) => this.toUrednik(),
    },{
      label: 'Затвори одредницу',
      command: (event) => this.toKraj(),
  }];

  addVariant(): void {
    this.variants.push({ nameE: '', nameI: '', extensionE: '', extensionI: '' });
  }

  removeVariant(variant): void {
    this.variants.splice(this.variants.indexOf(variant), 1);
  }

  selectedKindChangedHandler(selectedKind): void {
    this.selectedGender = selectedKind;
  }

  selectedVerbKindChangedHandler(selectedVerbKind): void {
    this.selectedVerbKind = selectedVerbKind;
  }

  selectedVerbFormChangedHandler(selectedVerbForm): void {
    this.selectedVerbForm = selectedVerbForm;
  }

  extensionChangedHandler(extension): void {
    this.extensionE = extension;
  }

  presentChangedHandler(presentE): void {
    this.presentE = presentE;
  }

  detailsChangedHandler(details): void {
    this.details = details;
  }

  collocationsChangedHandler(collocations): void {
    this.collocations = collocations;
  }

  selectedQualificatorsHandler(qualificators): void {
    this.qualificators = qualificators;
  }

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
    private route: ActivatedRoute,
    private odrednicaService: OdrednicaService,
    private previewService: PreviewService,
    private qualificatorService: QualificatorService,
    private enumService: EnumService,
    private tokenStorageService: TokenStorageService,
    private domSanitizer: DomSanitizer,
    private router: Router,
  ) {
    this.variants = [];
    this.isNoun = true;
    this.isVerb = false;
    this.selectedState = this.enumService.getEntryState(1);
    this.selectedWordType = this.enumService.getWordType(1);
  }

  close(): void {
    this.showInfoDialog = false;
    if (this.nextRoute) {
      this.router.navigate(this.nextRoute);
    }
  }

  yes(): void {
    this.yesHandler();
  }

  no(): void {
    this.showWarningDialog = false;
  }

  delete(): void {
    if (!this.editMode) {
      return;
    }
    this.message = 'Да ли сте сигурни да желите да обришете ову одредницу? Брисање се не може опозвати.';
    this.yesHandler = () => {
      this.odrednicaService.delete(this.id).subscribe(
        (status) => {
          this.showWarningDialog = false;
          this.message = 'Одредница је успешно обрисана.';
          this.showInfoDialog = true;
          this.nextRoute = ['/'];
        },
        (error) => {
          this.showWarningDialog = false;
          this.message = 'Грешка: ' + error;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  keyup(event, modelName: string, index = -1): void {
    if (event.key === 'F1') {
      this.accentCaretPos = event.target.selectionStart;
      this.accentIndex = index;
      if (this.accentCaretPos === 0) return;
      this.accentModelName = modelName;
      this.accentTarget = event.target;
      this.baseChar = event.target.value[this.accentCaretPos - 1];
      this.showAccentDialog = true;
    }
  }

  insertAccent(accent: string): void {
    const dotPos = this.accentModelName.indexOf('.');
    if (dotPos !== -1) {
      const attrName = this.accentModelName.slice(0, dotPos);
      const attrField = this.accentModelName.slice(dotPos + 1);
      const text = this[attrName][this.accentIndex][attrField];
      const newText = text.slice(0, this.accentCaretPos) + accent + text.slice(this.accentCaretPos);
      this[attrName][this.accentIndex][attrField] = newText;
    } else {
      const text = this[this.accentModelName];
      const newText = text.slice(0, this.accentCaretPos) + accent + text.slice(this.accentCaretPos);
      this[this.accentModelName] = newText;
    }
    this.showAccentDialog = false;
    this.accentTarget.focus();
    setTimeout(() => {this.accentTarget.setSelectionRange(this.accentCaretPos + 1, this.accentCaretPos + 1, 'none')});
  }

  save(): void {
    if (!this.check()) return;
    this.showWaitDialog = true;
    if (this.editMode) {
      this.odrednicaService.update(this.makeNewDeterminant()).subscribe(
        (data) => {
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Успешно aжурирана одредница.</p>');
          this.showWaitDialog = false;
          this.showInfoDialog = true;
          this.nextRoute = [];
          this.version += 1;
        },
        (error) => {
          console.log(error);
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом снимања одреднице: ${error}</p>`);
          this.showWaitDialog = false;
          this.showInfoDialog = true;
        });
    } else {
      this.odrednicaService.save(this.makeNewDeterminant()).subscribe(
        (data) => {
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Успешно додата нова одредница.</p>');
          this.showWaitDialog = false;
          this.showInfoDialog = true;
          this.nextRoute = ['/edit', data.id];
        },
        (error) => {
          console.log(error);
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Није могуће додати нову одредницу. Унесите све потребне податке.</p>');
          this.showWaitDialog = false;
          this.showInfoDialog = true;
        });
    }
  }

  finish(): void {
    if (!this.check()) return;
    this.message = this.domSanitizer.bypassSecurityTrustHtml(
      '<p>Операција још није имплементирана.</p>');
    this.showInfoDialog = true;
  }

  preview(): void {
    if (!this.check()) return;
    this.showWaitDialog = true;
    this.previewService.preview_backend(this.makeNewDeterminant()).subscribe(
      (data) => {
        this.message = this.domSanitizer.bypassSecurityTrustHtml(data);
        this.showWaitDialog = false;
        this.showInfoDialog = true;
        this.nextRoute = [];
      },
      (error) => {
        this.message = this.domSanitizer.bypassSecurityTrustHtml(
          '<p>Грешка у генерисању приказа одреднице.</p>');
        this.showWaitDialog = false;
        this.showInfoDialog = true;
      }
    );
  }

  onChangeWordType(): void {
    switch (this.selectedWordType.name) {
      case 'прилог':
      case 'узвик':
      case 'речца':
      case 'везник':
      case 'предлог':
      case 'придев':
        this.isVerb = false;
        this.isNoun = false;
        break;
      case 'именица':
      case 'заменица':
      case 'број':
        this.isVerb = false;
        this.isNoun = true;
        break;
      case 'глагол':
        this.isVerb = true;
        this.isNoun = false;
        this.selectedVerbForm = this.enumService.getVerbForm(0);
        this.selectedVerbKind = this.enumService.getVerbKind(0);
        break;
    }
  }

  def2visible(): boolean {
    if (!this.isVerb) {
      return false;
    }
    if (this.selectedVerbKind === undefined) {
      return false;
    }
    return this.selectedVerbKind.def2;
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.genders = this.enumService.getAllGenders();
    this.verbKinds = this.enumService.getAllVerbKinds();
    this.verbForms = this.enumService.getAllVerbForms();
    this.wordTypes = this.enumService.getAllWordTypes();
    const user = this.tokenStorageService.getUser();
    switch (user.group) {
      case 'Администратор':
        this.workflowItems = this.wfAdministrator;
        break;
      case 'Уредник':
        this.workflowItems = this.wfUrednik;
        break;
      case 'Редактор':
        this.workflowItems = this.wfRedaktor;
        break;
      case 'Обрађивач':
        this.workflowItems = this.wfObradjivac;
        break;
    }
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.id = null;
          this.selectedState = this.enumService.getEntryState(1);
          this.selectedWordType = this.enumService.getWordType(0);
          this.selectedVerbForm = this.enumService.getVerbForm(0);
          this.selectedVerbKind = this.enumService.getVerbKind(0);
          this.onChangeWordType();
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            this.odrednicaService.get(this.id).subscribe((value) => {
              this.fillForm(value);
              this.currentState = this.cloneState();
            });
          });
          break;
      }
    });
    this.dirty = false;
  }

  showError(message): void {
    this.message = this.domSanitizer.bypassSecurityTrustHtml(message);
    this.showInfoDialog = true;
  }

  assert(condition: boolean, message: string): void {
    if (condition) {
      this.showError(message);
      throw new Error();
    }
  }

  emptyVariant(): boolean {
    for (let v of this.variants) {
      if (v.nameE.trim().length === 0 && v.nameI.trim().length === 0 && v.extensionE.trim().length === 0 && v.extensionI.trim().length === 0)
        return true;
    }
    return false;
  }

  check(): boolean {
    try {
      this.assert(this.wordE === undefined || this.wordE.trim().length === 0, '<p>Обавезно је унети реч (основни облик одреднице).</p>');
      this.assert(this.selectedWordType?.id === 0 && !this.selectedGender, '<p>За именице је обавезно унети род.</p>');
      this.assert(this.emptyVariant(), '<p>Постоји (бар) једна празна варијанта.</p>');
      return true;
    } catch (e) {
      return false;
    }
  }

  makeNewDeterminant(): Determinant {
    const determinant: Determinant = {
      rec: this.wordE ? this.wordE.trim() : '',
      ijekavski: this.wordI ? this.wordI.trim() : null,
      varijante: this.variants.map((variant, index) => {
        return {
          redni_broj: index + 1,
          tekst: variant.nameE.trim(),
          ijekavski: variant.nameI.trim(),
          nastavak: variant.extensionE.trim(),
          nastavak_ij: variant.extensionI.trim(),
        };
      }),
      vrsta: this.selectedWordType?.id,
      rod: this.selectedGender?.id ? this.selectedGender?.id : null,
      nastavak: this.extensionE ? this.extensionE.trim() : '',
      nastavak_ij: this.extensionI ? this.extensionI.trim() : '',
      info: this.details ? this.details.trim() : '',
      glagolski_vid: this.selectedVerbForm?.id ? this.selectedVerbForm?.id : null,
      glagolski_rod: this.selectedVerbKind?.id ? this.selectedVerbKind?.id : null,
      prezent: this.presentE ? this.presentE.trim() : '',
      prezent_ij: this.presentI ? this.presentI.trim() : '',
      stanje: this.selectedState?.id ? this.selectedState?.id : 1,
      version: this.version,
      opciono_se: this.optionalSe,
      rbr_homonima: this.homonim === 0 ? null : this.homonim,
      kolokacije: this.collocations.map((c, i) => ({ redni_broj: i + 1, napomena: c.note, odrednice: c.determinants.map((d, j) => ({ odrednica_id: d.determinantId, redni_broj: j + 1}))})),
      sinonimi: this.synonyms.map((s, i) => ({redni_broj: i + 1, sinonim_id: s.determinantId})),
      antonimi: this.antonyms.map((a, i) => ({redni_broj: i + 1, antonim_id: a.determinantId})),
      kvalifikatori: this.qualificators.map((q, index) => {
        return {
          redni_broj: index + 1,
          kvalifikator_id: q.id,
          skracenica: q.abbreviation,
        };
      }),
      izrazi_fraze: this.expressions.map((value, idx) => {
        return {
          redni_broj: idx + 1,
          opis: value.value.trim(),
          tekst: value.tekst.trim(),
          vezana_odrednica_id: value.determinantId ? value.determinantId : null,
          kvalifikatori: value.qualificators.map((q, idx2) => {
            return {
              redni_broj: idx2 + 1,
              kvalifikator_id: q.id,
              skracenica: q.abbreviation,
            };
          })
        };
      }),
      znacenja: this.makeZnacenja(this.meanings, false).concat(this.makeZnacenja(this.meanings2, true)),
    };
    if (this.editMode) {
      determinant.id = this.id;
    }
    console.log('Sastavljeno za server:', determinant);
    return determinant;
  }

  makeZnacenja(meanings, znacenjeSe): any[] {
    return meanings ? meanings.map((z, index) => {
      return {
        redni_broj: index + 1,
        tekst: z.value.trim(),
        znacenje_se: znacenjeSe,
        podznacenja: z.submeanings.map((pz, idx) => {
          return {
            redni_broj: idx + 1,
            tekst: pz.value.trim(),
            izrazi_fraze: pz.expressions.map((value, idx2) => {
              return {
                redni_broj: idx2 + 1,
                opis: value.value.trim(),
                tekst: value.tekst.trim(),
                vezana_odrednica_id: value.determinantId ? value.determinantId : null,
              };
            }),
            kvalifikatori: pz.qualificators.map((q, idx2) => {
              return {
                redni_broj: idx2 + 1,
                kvalifikator_id: q.id,
                skracenica: q.abbreviation
              };
            }),
            konkordanse: pz.concordances.map((c, idx2) => {
              return {
                redni_broj: idx2 + 1,
                opis: c.concordance.trim(),
                publikacija_id: c.bookId ? c.bookId : null,
              };
            }),
          };
        }),
        izrazi_fraze: z.expressions.map((value, idx) => {
          return {
            redni_broj: idx + 1,
            opis: value.value.trim(),
            tekst: value.tekst.trim(),
            vezana_odrednica_id: value.determinantId ? value.determinantId : null,
          };
        }),
        kvalifikatori: z.qualificators.map((q, idx) => {
          return {
            redni_broj: idx + 1,
            kvalifikator_id: q.id,
            skracenica: q.abbreviation
          };
        }),
        konkordanse: z.concordances.map((c, idx) => {
          return {
            redni_broj: idx + 1,
            opis: c.concordance.trim(),
            publikacija_id: c.bookId ? c.bookId : null,
          };
        }),
      };
    }) : [];
  }

  fillForm(value: any): void {
    console.log('Procitano sa servera:', value);
    this.id = value.id;
    this.version = value.version;
    this.wordE = value.rec;
    this.wordI = value.ijekavski;
    this.extensionE = value.nastavak;
    this.extensionI = value.nastavak_ij;
    for (const v of value.varijantaodrednice_set) {
      this.variants.push({ nameE: v.tekst, nameI: v.ijekavski, extensionE: v.nastavak, extensionI: v.nastavak_ij });
    }
    this.selectedState = this.enumService.getEntryState(value.stanje);
    this.selectedWordType = this.enumService.getWordType(value.vrsta);
    this.optionalSe = value.opciono_se;
    this.homonim = value.rbr_homonima;
    switch (value.vrsta) {
      case 0:
        this.selectedGender = this.enumService.getGender(value.rod);
      // tslint:disable-next-line:no-switch-case-fall-through
      case 5:
      case 2:
      case 9:
        this.isNoun = true;
        this.isVerb = false;
        break;
      case 1:
        this.selectedVerbForm = this.enumService.getVerbForm(value.glagolski_vid);
        this.selectedVerbKind = this.enumService.getVerbKind(value.glagolski_rod);
        this.presentE = value.prezent;
        this.presentI = value.prezent_ij;
        this.isNoun = false;
        this.isVerb = true;
        break;
      default:
        this.isNoun = false;
        this.isVerb = false;
        break;
    }
    this.details = value.info === null ? '' : value.info;
    this.meanings = this.makeMeanings(value.znacenje_set.filter(z => !z.znacenje_se));
    this.meanings2 = this.makeMeanings(value.znacenje_set.filter(z => z.znacenje_se));
    this.expressions = value.izrazfraza_set.map((expr) => ({
      value: expr.opis,
      tekst: expr.tekst,
      determinantId: expr.vezana_odrednica_id,
      searchText: '',
      rec$: undefined,
      qualificators: expr.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id))
    }));
    this.qualificators = value.kvalifikatorodrednice_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
    this.collocations = value.kolokacija_set.map((k) => ({note: k.napomena, determinants: k.recukolokaciji_set.map((r) => ({ determinantId: r.odrednica_id, searchText: '', rec$: undefined }))}));
    this.synonyms = value.ima_sinonim.map((s) => ({ determinantId: s.u_vezi_sa_id, searchText: '', rec$: undefined}));
    this.antonyms = value.ima_antonim.map((s) => ({ determinantId: s.u_vezi_sa_id, searchText: '', rec$: undefined}));
  }

  fillTestOdrednica(odrednica): void {
    if (this.editMode) {
      this.message = 'Унос примера одреднице могућ је само у режиму уноса нове одреднице, не и уређивања постојеће.';
      this.showInfoDialog = true;
      this.nextRoute = [];
      return;
    }
    this.fillForm(odrednica);
  }

  makeMeanings(znacenja): any[] {
    return znacenja.map(z => ({
      value: z.tekst,
      expressions: z.izrazfraza_set.map((e) => {
        return {
          value: e.opis,
          tekst: e.tekst,
          determinantId: e.vezana_odrednica_id,
          searchText: '',
          rec$: undefined,
          qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        };
      }),
      qualificators: z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
      concordances: z.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
      submeanings: z.podznacenje_set.map((pz) => ({
        value: pz.tekst,
        expressions: pz.izrazfraza_set.map((e, idx) => {
          return {
            value: e.opis,
            tekst: e.tekst,
            determinantId: e.vezana_odrednica_id,
            searchText: '',
            rec$: undefined,
            qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
          };
        }),
        qualificators: pz.kvalifikatorpodznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        concordances: pz.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
    }))}));
  }

  isQualificator(obj: any): boolean {
    return 'id' in obj && 'name' in obj && 'abbreviation' in obj;
  }

  clone(srcObj: any): any {
    if (!srcObj)
      return srcObj;
    if (typeof srcObj === 'string')
      return `${srcObj}`;
    if (['number', 'boolean', 'bigint'].includes(typeof srcObj))
      return srcObj;
    if (this.isQualificator(srcObj))
      return srcObj;
    if (Array.isArray(srcObj)) {
      const arr = Object.assign([], srcObj);
      for (let i = 0; i < arr.length; i++)
        arr[i] = this.clone(srcObj[i]);
      return arr;
    }
    const cloneObj = Object.assign({}, srcObj);
    for (const attr in srcObj) {
      if (attr.endsWith('$'))
        cloneObj[attr] = undefined;
      else
        cloneObj[attr] = this.clone(srcObj[attr]);
    }
    return cloneObj;
  }

  cloneState(): any {
    const stateObj = {
      id: this.id,
      version: this.version,
      wordE: this.clone(this.wordE),
      wordI: this.clone(this.wordI),
      extensionE: this.clone(this.extensionE),
      extensionI: this.clone(this.extensionI),
      variants: this.clone(this.variants),
      selectedWordType: this.selectedWordType,
      selectedState: this.selectedState,
      optionalSe: this.clone(this.optionalSe),
      homonim: this.clone(this.homonim),
      selectedGender: this.selectedGender,
      isNoun: this.isNoun,
      isVerb: this.isVerb,
      selectedVerbKind: this.selectedVerbKind,
      selectedVerbForm: this.selectedVerbForm,
      presentE: this.clone(this.presentE),
      presentI: this.clone(this.presentI),
      details: this.clone(this.details),
      meanings: this.clone(this.meanings),
      meanings2: this.clone(this.meanings2),
      expressions: this.clone(this.expressions),
      qualificators: this.clone(this.qualificators),
      collocations: this.clone(this.collocations),
      antonyms: this.clone(this.antonyms),
      synonyms: this.clone(this.synonyms),
    };
    return stateObj;
  }

  setState(stateObj): void {
    this.id = stateObj.id;
    this.version = stateObj.version;
    this.wordE = stateObj.wordE;
    this.wordI = stateObj.wordI;
    this.extensionE = stateObj.extensionE;
    this.extensionI = stateObj.extensionI;
    this.variants = stateObj.variants;
    this.selectedWordType = stateObj.selectedWordType;
    this.selectedState = stateObj.selectedState;
    this.optionalSe = stateObj.optionalSe;
    this.homonim = stateObj.homonim;
    this.selectedGender = stateObj.selectedGender;
    this.isNoun = stateObj.isNoun;
    this.isVerb = stateObj.isVerb;
    this.selectedVerbKind = stateObj.selectedVerbKind;
    this.selectedVerbForm = stateObj.selectedVerbForm;
    this.presentE = stateObj.presentE;
    this.presentI = stateObj.presentI;
    this.details = stateObj.details;
    this.meanings = stateObj.meanings;
    this.meanings2 = stateObj.meanings2;
    this.expressions = stateObj.expressions;
    this.qualificators = stateObj.qualificators;
    this.collocations = stateObj.collocations;
    this.antonyms = stateObj.antonyms;
    this.synonyms = stateObj.synonyms;
  }

  saveChange(): void {
    this.undoStack.push(this.currentState);
    console.log('Pre:', this.currentState);
    this.currentState = this.cloneState();
    console.log('Posle:', this.currentState);
    this.redoStack = [];
  }

  undo(): void {
    if (this.undoStack.length > 0) {
      this.redoStack.push(this.cloneState());
      this.currentState = this.undoStack.pop();
      this.setState(this.currentState);
    }
  }

  redo(): void {
    if (this.redoStack.length > 0) {
      this.undoStack.push(this.currentState);
      this.currentState = this.redoStack.pop();
      this.setState(this.currentState);
    }
  }

  undoAvailable(): boolean {
    return this.undoStack.length > 0;
  }

  redoAvailable(): boolean {
    return this.redoStack.length > 0;
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.saveChange();
      this.dirty = false;
    }
  }

  toObradjivac(): void {
    if (!this.editMode)
      return;
    this.message = 'Да ли сте сигурни да желите да проследите одредницу обрађивачу?';
    this.yesHandler = () => {
      this.odrednicaService.toObradjivac(this.id).subscribe(
        (success) => {
          this.showWarningDialog = false;
          this.message = 'Одредница је прослеђена обрађивачу.';
          this.showInfoDialog = true;
          this.nextRoute = ['/'];
        },
        (error) => {
          this.showWarningDialog = false;
          this.message = 'Грешка: ' + error;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  toRedaktor(): void {
    if (!this.editMode)
      return;
    this.message = 'Да ли сте сигурни да желите да проследите одредницу редактору?';
    this.yesHandler = () => {
      this.odrednicaService.toRedaktor(this.id).subscribe(
        (success) => {
          this.showWarningDialog = false;
          this.message = 'Одредница је прослеђена редактору.';
          this.showInfoDialog = true;
          this.nextRoute = ['/'];
        },
        (error) => {
          this.showWarningDialog = false;
          this.message = 'Грешка: ' + error;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  toUrednik(): void {
    if (!this.editMode)
      return;
    this.message = 'Да ли сте сигурни да желите да проследите одредницу уреднику?';
    this.yesHandler = () => {
      this.odrednicaService.toUrednik(this.id).subscribe(
        (success) => {
          this.showWarningDialog = false;
          this.message = 'Одредница је прослеђена уреднику.';
          this.showInfoDialog = true;
          this.nextRoute = ['/'];
        },
        (error) => {
          this.showWarningDialog = false;
          this.message = 'Грешка: ' + error;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  toKraj(): void {
    if (!this.editMode)
      return;
    this.message = 'Да ли сте сигурни да желите да затворите одредницу?'
    this.showWarningDialog = true;
    this.yesHandler = () => {
      this.odrednicaService.toKraj(this.id).subscribe(
        (success) => {
          this.showWarningDialog = false;
          this.message = 'Одредница је затворена за обраду.';
          this.showInfoDialog = true;
          this.nextRoute = ['/'];
        },
        (error) => {
          this.showWarningDialog = false;
          this.message = 'Грешка: ' + error;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }
}

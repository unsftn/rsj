import { Component, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { MenuItem, PrimeNGConfig } from 'primeng/api';
import {
  Gender,
  StanjeOdrednice,
  Determinant,
  Qualificator,
  VerbKind,
  VerbForm,
  WordType,
  DeterminantStatus
} from '../../models';
import { OdrednicaService, PreviewService, QualificatorService, EnumService } from '../../services/odrednice';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import {UserService} from '../../services/auth/user.service';

interface Variant {
  nameE: string;
  nameI: string;
  extensionE: string;
  extensionI: string;
  presentE: string;
  presentI: string;
  optionalSe: boolean;
  gender: Gender;
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
  selectedStatus: DeterminantStatus;
  statuses: DeterminantStatus[];
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
  changes: any[];
  notes: string;
  freetext: string;

  errorMsg: string;
  showInfoDialog = false;
  showWarningDialog = false;
  showWaitDialog = false;
  showAccentDialog = false;
  showOwnershipDialog = false;
  accentChar = 'а';
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

  groupId = 0;
  obradjivac: any = null;
  redaktor: any = null;
  urednik: any = null;
  obradjivaci: any[] = [];
  redaktori: any[] = [];
  urednici: any[] = [];

  workflowItems: MenuItem[];
  wfObradjivac: MenuItem[] = [{
      label: 'Проследи редактору',
      command: (event) => this.toRedaktor(),
    },{
      label: 'Задужења',
      command: (event) => this.showOwnership(),
  }];
  wfRedaktor: MenuItem[] = [{
      label: 'Врати на обраду',
      command: (event) => this.toObradjivac(),
    },{
      label: 'Проследи уреднику',
      command: (event) => this.toUrednik(),
    },{
      label: 'Задужења',
      command: (event) => this.showOwnership(),
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
    },{
      label: 'Задужења',
      command: (event) => this.showOwnership(),
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
    },{
      label: 'Задужења',
      command: (event) => this.showOwnership(),
  }];

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
    private userService: UserService,
    private titleService: Title,
  ) {
    this.variants = [];
    this.isNoun = true;
    this.isVerb = false;
    this.selectedState = this.enumService.getEntryState(1);
    this.selectedWordType = this.enumService.getWordType(1);
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
        this.groupId = 4;
        break;
      case 'Уредник':
        this.workflowItems = this.wfUrednik;
        this.groupId = 3;
        break;
      case 'Редактор':
        this.workflowItems = this.wfRedaktor;
        this.groupId = 2;
        break;
      case 'Обрађивач':
        this.workflowItems = this.wfObradjivac;
        this.groupId = 1;
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
          this.selectedStatus = null;
          this.onChangeWordType();
          this.titleService.setTitle('Нова одредница');
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
    this.odrednicaService.getStatuses().subscribe(data => {
      this.statuses = data;
      if (!this.selectedStatus)
        this.selectedStatus = this.statuses[0];
    }, error => {
      console.log(error);
    });
    if (this.obradjivaci.length === 0)
      this.obradjivaci = this.userService.getObradjivaci();
    if (this.redaktori.length === 0)
      this.redaktori = this.userService.getRedaktori();
    if (this.urednici.length === 0)
      this.urednici = this.userService.getUrednici();
    this.dirty = false;
  }

  getStatus(id: number): DeterminantStatus {
    if (id === null)
      return null;
    for (const st of this.statuses)
      if (st.id === id)
        return st;
    return null;
  }

  addVariant(): void {
    this.variants.push({ nameE: '', nameI: '', extensionE: '', extensionI: '', presentE: '', presentI: '', optionalSe: false, gender: null });
  }

  removeVariant(variant): void {
    this.variants.splice(this.variants.indexOf(variant), 1);
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
          const errorMessage = sessionStorage.getItem('errorMessage');
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом брисања одреднице:<br/> <b>${errorMessage}</b></p>`);
          this.showWarningDialog = false;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  keyup(event, modelName: string, index = -1): void {
    if (event.key === 'F1' || event.key === 'F4') {
      this.accentCaretPos = event.target.selectionStart;
      this.accentIndex = index;
      if (this.accentCaretPos === 0) return;
      this.accentModelName = modelName;
      this.accentTarget = event.target;
      this.accentChar = event.target.value[this.accentCaretPos - 1];
      this.showAccentDialog = true;
    }
  }

  @HostListener("window:keyup", ["$event"])
  keyEvent(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      if (this.showWarningDialog) {
        this.yes();
      } else if (this.showInfoDialog) {
        this.close();
      } else if (this.showOwnershipDialog) {
        this.saveOwnership();
      }
    } else if (event.key === 'Esc') {
      if (this.showWarningDialog) {
        this.no();
      } else if (this.showInfoDialog) {
        this.close();
      } else if (this.showOwnershipDialog) {
        this.closeOwnership();
      }
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
    setTimeout(() => { this.accentTarget.setSelectionRange(this.accentCaretPos + 1, this.accentCaretPos + 1, 'none'); });
  }

  checkDuplicate(showAllowSave: boolean): void {
    if (this.showAccentDialog)
      return;
    if (this.wordE === undefined)
      return;
    this.odrednicaService.checkDuplicate(this.wordE, this.id, this.homonim).subscribe(data => {
      if (data.length > 0) {
        console.log(data);
        if (showAllowSave) {
          console.log('prikazi pitanje za save');
        } else {
          this.showError('Ова одредница је већ унета!');
        }
      }
    });
  }

  save(): void {
    if (!this.check()) return;
    const saveDeterminant = () => {
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
            const errorMessage = sessionStorage.getItem('errorMessage');
            this.message = this.domSanitizer.bypassSecurityTrustHtml(
              `<p>Грешка приликом снимања одреднице:<br/> <b>${errorMessage}</b></p>`);
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
            const errorMessage = sessionStorage.getItem('errorMessage');
            this.message = this.domSanitizer.bypassSecurityTrustHtml(
              `<p>Грешка приликом снимања одреднице:<br/> <b>${errorMessage}</b></p>`);
            this.showWaitDialog = false;
            this.showInfoDialog = true;
          });
      }
    };
    this.odrednicaService.checkDuplicate(this.wordE, this.id, this.homonim).subscribe(data => {
      if (data.length > 0) {
        this.yesHandler = saveDeterminant;
        this.message = 'Ова одредница је већ унета! Да ли желите да је сачувате као дупликат?';
        this.showWarningDialog = true;
      } else {
        saveDeterminant();
      }
    });
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
        const errorMessage = sessionStorage.getItem('errorMessage');
        this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка у генерисању приказа одреднице.<br/> <b>${errorMessage}</b></p>`);
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

  showError(message: string): void {
    this.message = this.domSanitizer.bypassSecurityTrustHtml(message);
    this.showInfoDialog = true;
  }

  showWarning(message: string): void {
    this.message = this.domSanitizer.bypassSecurityTrustHtml(message);
    this.showWarningDialog = true;
  }

  assert(condition: boolean, message: string): void {
    if (condition) {
      this.showError(message);
      throw new Error();
    }
  }

  emptyVariant(): boolean {
    for (const v of this.variants) {
      if (this.isVerb) {
        if (v.nameE.trim().length === 0 && v.nameI.trim().length === 0 && v.extensionE.trim().length === 0 && v.extensionI.trim().length === 0 && v.presentE.trim().length === 0 && v.presentI.trim().length === 0)
          return true;
      } else {
        if (v.nameE.trim().length === 0 && v.nameI.trim().length === 0 && v.extensionE.trim().length === 0 && v.extensionI.trim().length === 0)
          return true;
      }
    }
    return false;
  }

  emptyDeterminant(dets: any[]): boolean {
    for (const s of dets) {
      if (!s.determinantId && !s.text)
        return true;
    }
    return false;
  }

  emptySynonym(): boolean {
    return this.emptyDeterminant(this.synonyms);
  }

  emptyAntonym(): boolean {
    return this.emptyDeterminant(this.antonyms);
  }

  emptyCollocation(): boolean {
    for (const c of this.collocations) {
      if (this.emptyDeterminant(c.determinants))
        return true;
    }
    return false;
  }

  emptyShortCollocation(): boolean {
    for (const z of this.meanings) {
      for (const coll of z.collocations) {
        if (!coll.tekst)
          return true;
        for (const podz of z.submeanings) {
          for (const coll2 of podz.collocations) {
            if (!coll2.tekst)
              return true;
          }
        }
      }
    }
    return false;
  }

  check(): boolean {
    try {
      this.assert(this.wordE === undefined || this.wordE.trim().length === 0, '<p>Обавезно је унети реч (основни облик одреднице).</p>');
      this.assert(this.selectedWordType?.id === 0 && !this.selectedGender, '<p>За именице је обавезно унети род.</p>');
      this.assert(this.emptyVariant(), '<p>Постоји (бар) једна празна варијанта.</p>');
      this.assert(this.emptySynonym(), '<p>Постоји (бар) један празан синоним.</p>');
      this.assert(this.emptyAntonym(), '<p>Постоји (бар) један празан антоним.</p>');
      this.assert(this.emptyCollocation(), '<p>Постоји (бар) једна празна одредница у колокацијама.</p>');
      this.assert(this.emptyShortCollocation(), '<p>Постоји (бар) једна празна колокација у оквиру значења, подзначења или фразе.</p>');
      return true;
    } catch (e) {
      console.log(e);
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
          prezent: variant.presentE.trim(),
          prezent_ij: variant.presentI.trim(),
          opciono_se: variant.optionalSe,
          rod: variant.gender?.id ? variant.gender?.id : null,
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
      status_id: this.selectedStatus === null ? null : this.selectedStatus.id,
      kolokacije: this.collocations.map((c, i) => ({ redni_broj: i + 1, napomena: c.note, odrednice: c.determinants.map((d, j) => ({ odrednica_id: d.determinantId, redni_broj: j + 1, tekst: d.text}))})),
      sinonimi: this.synonyms.map((s, i) => ({redni_broj: i + 1, sinonim_id: s.determinantId, tekst: s.text})),
      antonimi: this.antonyms.map((a, i) => ({redni_broj: i + 1, antonim_id: a.determinantId, tekst: a.text})),
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
          konkordanse: value.concordances.map((c, idx2) => {
            return {
              redni_broj: idx2 + 1,
              opis: c.concordance.trim(),
              publikacija_id: c.bookId ? c.bookId : null,
            };
          }),
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
      napomene: this.notes ? this.notes.trim() : '',
      freetext: this.freetext ? this.freetext.trim() : '',
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
                konkordanse: value.concordances.map((c, idx3) => {
                  return {
                    redni_broj: idx3 + 1,
                    opis: c.concordance.trim(),
                    publikacija_id: c.bookId ? c.bookId : null,
                  };
                }),
                kvalifikatori: value.qualificators.map((q, idx3) => {
                  return {
                    redni_broj: idx3 + 1,
                    kvalifikator_id: q.id,
                    skracenica: q.abbreviation
                  };
                }),
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
            kolokacije: pz.collocations.map((coll, idx2) => {
              return {
                redni_broj: idx2 + 1,
                tekst: coll.tekst
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
            konkordanse: value.concordances.map((c, idx2) => {
              return {
                redni_broj: idx2 + 1,
                opis: c.concordance.trim(),
                publikacija_id: c.bookId ? c.bookId : null,
              };
            }),
            kvalifikatori: value.qualificators.map((q, idx2) => {
              return {
                redni_broj: idx2 + 1,
                kvalifikator_id: q.id,
                skracenica: q.abbreviation
              };
            }),
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
        kolokacije: z.collocations.map((coll, idx) => {
          return {
            redni_broj: idx + 1,
            tekst: coll.tekst
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
    this.titleService.setTitle(value.rec);
    this.wordI = value.ijekavski;
    this.extensionE = value.nastavak;
    this.extensionI = value.nastavak_ij;
    this.variants = [];
    for (const v of value.varijantaodrednice_set) {
      this.variants.push({ nameE: v.tekst, nameI: v.ijekavski, extensionE: v.nastavak, extensionI: v.nastavak_ij, presentE: v.prezent, presentI: v.prezent_ij, optionalSe: v.opciono_se ? true : false, gender: this.enumService.getGender(v.rod) });
    }
    this.selectedState = this.enumService.getEntryState(value.stanje);
    this.selectedWordType = this.enumService.getWordType(value.vrsta);
    this.optionalSe = value.opciono_se;
    this.homonim = value.rbr_homonima;
    this.selectedStatus = this.getStatus(value.status);
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
      concordances: expr.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
      qualificators: expr.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id))
    }));
    this.qualificators = value.kvalifikatorodrednice_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
    this.collocations = value.kolokacija_set.map((k) => ({note: k.napomena, determinants: k.recukolokaciji_set.map((r) => ({ determinantId: r.odrednica_id, searchText: '', rec$: undefined, text: r.tekst }))}));
    this.synonyms = value.ima_sinonim.map((s) => ({ determinantId: s.u_vezi_sa_id, searchText: '', rec$: undefined, text: s.tekst}));
    this.antonyms = value.ima_antonim.map((s) => ({ determinantId: s.u_vezi_sa_id, searchText: '', rec$: undefined, text: s.tekst}));
    this.changes = value.izmenaodrednice_set;
    this.notes = value.napomene;
    this.freetext = value.freetext;
    if (value.obradjivac)
      this.obradjivac = this.userService.getUser(value.obradjivac);
    else
      this.obradjivac = null;
    if (value.redaktor)
      this.redaktor = this.userService.getUser(value.redaktor);
    else
      this.redaktor = null;
    if (value.urednik)
      this.urednik = this.userService.getUser(value.urednik);
    else
      this.urednik = null;
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
          concordances: e.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
          qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        };
      }),
      qualificators: z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
      concordances: z.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
      collocations: z.kolokacijaznacenja_set.map((kol) => ({tekst: kol.tekst})),
      submeanings: z.podznacenje_set.map((pz) => ({
        value: pz.tekst,
        expressions: pz.izrazfraza_set.map((e, idx) => {
          return {
            value: e.opis,
            tekst: e.tekst,
            determinantId: e.vezana_odrednica_id,
            searchText: '',
            rec$: undefined,
            concordances: e.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
            qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
          };
        }),
        qualificators: pz.kvalifikatorpodznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        concordances: pz.konkordansa_set.map((k) => ({concordance: k.opis, bookId: k.publikacija_id, searchText: '', naslov$: undefined, skracenica$: undefined})),
        collocations: pz.kolokacijapodznacenja_set.map((kol) => ({tekst: kol.tekst})),
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
    this.currentState = this.cloneState();
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
          const errorMessage = sessionStorage.getItem('errorMessage');
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом прослеђивања одреднице:<br/> <b>${errorMessage}</b></p>`);
          this.showWarningDialog = false;
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
          const errorMessage = sessionStorage.getItem('errorMessage');
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом прослеђивања одреднице:<br/> <b>${errorMessage}</b></p>`);
          this.showWarningDialog = false;
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
          const errorMessage = sessionStorage.getItem('errorMessage');
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом прослеђивања одреднице:<br/> <b>${errorMessage}</b></p>`);
          this.showWarningDialog = false;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  toKraj(): void {
    if (!this.editMode)
      return;
    this.message = 'Да ли сте сигурни да желите да затворите одредницу?';
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
          const errorMessage = sessionStorage.getItem('errorMessage');
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом прослеђивања одреднице:<br/> <b>${errorMessage}</b></p>`);
          this.showWarningDialog = false;
          this.showInfoDialog = true;
          this.nextRoute = [];
        });
    };
    this.showWarningDialog = true;
  }

  showOwnership(): void {
    if (!this.editMode)
      return;
    this.showOwnershipDialog = true;
  }

  saveOwnership(): void {
    if (this.groupId === 1) {
      this.showOwnershipDialog = false;
      return;
    }
    const obradjivacId = this.obradjivac.id;
    const redaktorId = this.redaktor ? this.redaktor.id : null;
    const urednikId = this.urednik ? this.urednik.id : null;
    this.odrednicaService.zaduzenja(this.id, obradjivacId, redaktorId, urednikId).subscribe(
      (data) => {
        this.showOwnershipDialog = false;
      },
      (error) => {
        console.log(error);
        this.showOwnershipDialog = false;
      }
    );
  }

  closeOwnership(): void {
    this.showOwnershipDialog = false;
  }
}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Gender, StanjeOdrednice, Determinant, Qualificator, VerbKind, VerbForm, WordType } from '../../models';
import { OdrednicaService, PreviewService, QualificatorService, EnumService } from '../../services/odrednice';
import { ODREDNICA_1, ODREDNICA_2, ODREDNICA_3, ODREDNICA_4 } from '../../examples';

interface Variant {
  nameE: string;
  nameI: string;
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
  extension;
  variants: Variant[];

  genders: Gender[];
  verbKinds: VerbKind[];
  verbForms: VerbForm[];

  selectedVerbKind: VerbKind;
  selectedVerbForm: VerbForm;
  present: string;
  details;
  collocations;

  selectedWordType: WordType;
  selectedState: StanjeOdrednice;
  qualificators: Qualificator[] = [];
  id: number;
  editMode: boolean;  // false: nova odrednica; true: edit postojece
  version = 1;
  optionalSe: boolean;

  meanings: any[] = [];
  meanings2: any[] = [];
  expressions: any[] = [];

  errorMsg: string;
  showInfoDialog = false;
  showWarningDialog = false;
  message: SafeHtml;
  nextRoute: any[];

  addVariant(): void {
    this.variants.push({nameE: '', nameI: ''});
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
    this.extension = extension;
  }

  presentChangedHandler(present): void {
    this.present = present;
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
    this.odrednicaService.delete(this.id).subscribe(
      (status) => {
        this.showWarningDialog = false;
        this.message = 'Одредница је успешно обрисана.';
        this.showInfoDialog = true;
        this.nextRoute = ['/']
      }, (error) => {
        this.showWarningDialog = false;
        this.message = 'Грешка: ' + error;
        this.showInfoDialog = true;
        this.nextRoute = [];
      });
  }

  no(): void {
    this.showWarningDialog = false;
  }

  delete(): void {
    if (!this.editMode) {
      return;
    }
    this.message = 'Да ли сте сигурни да желите да обришете ову одредницу? Брисање се не може опозвати.';
    this.showWarningDialog = true;
  }

  save(): void {
    if (this.editMode) {
      this.odrednicaService.update(this.makeNewDeterminant()).subscribe(
        (data) => {
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Успешно aжурирана одредница.</p>');
          this.showInfoDialog = true;
          this.nextRoute = [];
        },
        (error) => {
          console.log(error);
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            `<p>Грешка приликом снимања одреднице: ${error}</p>`);
          this.showInfoDialog = true;
        });

    } else {
      this.odrednicaService.save(this.makeNewDeterminant()).subscribe(
        (data) => {
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Успешно додата нова одредница.</p>');
          this.showInfoDialog = true;
          this.nextRoute = ['/edit', data.id];
        },
        (error) => {
          console.log(error);
          this.message = this.domSanitizer.bypassSecurityTrustHtml(
            '<p>Није могуће додати нову одредницу. Унесите све потребне податке.</p>');
          this.showInfoDialog = true;
        });
    }
  }

  finish(): void {
    this.message = this.domSanitizer.bypassSecurityTrustHtml(
      '<p>Операција још није имплементирана.</p>');
    this.showInfoDialog = true;
  }

  preview(): void {
    const tekst = this.previewService.preview(this.makeNewDeterminant());
    this.message = this.domSanitizer.bypassSecurityTrustHtml(tekst);
    this.showInfoDialog = true;
    this.nextRoute = [];
  }

  onChangeWordType(): void {
    switch (this.selectedWordType.name) {
      case 'прилог':
      case 'узвик':
      case 'речца':
      case 'везник':
      case 'предлог':
        this.isVerb = false;
        this.isNoun = false;
        break;
      case 'именица':
      case 'заменица':
      case 'придев':
      case 'број':
        this.isVerb = false;
        this.isNoun = true;
        break;
      case 'глагол':
        this.isVerb = true;
        this.isNoun = false;
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
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.id = null;
          this.selectedState = this.enumService.getEntryState(1);
          this.selectedWordType = this.enumService.getWordType(0);
          this.onChangeWordType();
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            this.odrednicaService.get(this.id).subscribe((value) => {
              this.fillForm(value);
            });
          });
          break;
      }
    });
  }

  makeNewDeterminant(): Determinant {
    const determinant: Determinant = {
      rec: this.wordE,
      ijekavski: this.wordI,
      varijante: this.variants.map((variant, index) => {
        return {
          redni_broj: index + 1,
          tekst: variant.nameE,
          ijekavski: variant.nameI,
        };
      }),
      vrsta: this.selectedWordType?.id,
      rod: this.selectedGender?.id ? this.selectedGender?.id : null,
      nastavak: this.extension ? this.extension : '',
      info: this.details ? this.details : '',
      glagolski_vid: this.selectedVerbForm?.id ? this.selectedVerbForm?.id : 0,
      glagolski_rod: this.selectedVerbKind?.id ? this.selectedVerbKind?.id : 0,
      prezent: this.present ? this.present : '',
      stanje: this.selectedState?.id ? this.selectedState?.id : 1,
      version: this.version,
      opciono_se: this.optionalSe,
      kolokacija_set: this.collocations ? this.collocations : [],
      kvalifikatori: this.qualificators.map((q, index) => {
        return {
          redni_broj: index + 1,
          kvalifikator_id: q.id,
          skracenica: q.abbreviation
        };
      }),
      izrazi_fraze: this.expressions.map((value, idx) => {
        return {
          redni_broj: idx + 1,
          opis: value.value,
          tekst: value.tekst,
          kvalifikatori: value.qualificators.map((q, idx2) => {
            return {
              redni_broj: idx2 + 1,
              kvalifikator_id: q.id,
              skracenica: q.abbreviation,
            };
          })
        };
      }),
      znacenja: this.meanings ? this.meanings.map((z, index) => {
        return {
          redni_broj: index + 1,
          tekst: z.value,
          podznacenja: z.submeanings.map((pz, idx) => {
            return {
              redni_broj: idx + 1,
              tekst: pz.value,
              izrazi_fraze: pz.expressions.map((value, idx2) => {
                return {
                  redni_broj: idx2 + 1,
                  opis: value.value,
                  tekst: value.tekst,
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
                  opis: c.concordance,
                };
              }),
            };
          }),
          izrazi_fraze: z.expressions.map((value, idx) => {
            return {
              redni_broj: idx + 1,
              opis: value.value,
              tekst: value.tekst,
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
              opis: c.concordance,
            };
          }),
        };
      }) : [],
    };
    if (this.editMode) {
      determinant.id = this.id;
    }
    console.log('Sastavljeno za server:', determinant);
    return determinant;
  }

  fillForm(value: any): void {
    console.log('Procitano sa servera:', value);
    this.id = value.id;
    this.version = value.version;
    this.wordE = value.rec;
    this.wordI = value.ijekavski;
    for (const v of value.varijantaodrednice_set) {
      this.variants.push({nameE: v.tekst, nameI: v.ijekavski});
    }
    this.selectedState = this.enumService.getEntryState(value.stanje);
    this.selectedWordType = this.enumService.getWordType(value.vrsta);
    this.optionalSe = value.opciono_se;
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
        this.present = value.prezent;
        this.isNoun = false;
        this.isVerb = true;
        break;
      default:
        this.isNoun = false;
        this.isVerb = false;
        break;
    }
    this.details = value.info === null ? '' : value.info;
    this.meanings = [];
    for (const z of value.znacenje_set) {
      const obj = {
        value: z.tekst,
        submeanings: [],
        expressions: z.izrazfraza_set.map((e) => {
          return {
            value: e.opis,
            tekst: e.tekst,
            keywords: [],
            qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
          };
        }),
        qualificators: z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        concordances: z.konkordansa_set.map((k) => ({concordance: k.opis})),
      };
      for (const pz of z.podznacenje_set) {
        obj.submeanings.push({
          value: pz.tekst,
          expressions: pz.izrazfraza_set.map((e, idx) => {
            return {
              value: e.opis,
              tekst: e.tekst,
              keywords: [],
              qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
            };
          }),
          qualificators: pz.kvalifikatorpodznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
          concordances: pz.konkordansa_set.map((k) => ({concordance: k.opis})),
        });
      }
      this.meanings.push(obj);
    }
    this.expressions = value.izrazfraza_set.map((expr) => ({
      value: expr.opis,
      tekst: expr.tekst,
      keywords: [],
      qualificators: expr.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id))
    }));
    this.qualificators = value.kvalifikatorodrednice_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
  }

  fillTestOdrednica1(): void {
    this.fillForm(ODREDNICA_1);
  }

  fillTestOdrednica2(): void {
    this.fillForm(ODREDNICA_2);
  }

  fillTestOdrednica3(): void {
    this.fillForm(ODREDNICA_3);
  }

  fillTestOdrednica4(): void {
    this.fillForm(ODREDNICA_4);
  }
}

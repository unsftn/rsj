import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Gender, StanjeOdrednice, Determinant, Qualificator, VerbKind, VerbForm, WordType } from '../../models';
import { OdrednicaService, PreviewService, QualificatorService, EnumService } from '../../services/odrednice';

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
  display = false;
  message: SafeHtml;
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
  formMode: number;  // 1 - nova odrednica; 2 - edit postojece
  optionalSe: boolean;

  meanings: any[] = [];
  meanings2: any[] = [];
  expressions: any[] = [];

  addVariant(): void {
    this.variants.push({ nameE: '', nameI: '' });
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
  ) {
    this.variants = [];
    this.isNoun = true;
    this.isVerb = false;
    this.selectedState = this.enumService.getEntryState(1);
    this.selectedWordType = this.enumService.getWordType(1);
  }

  async save(): Promise<void> {
    if (this.formMode === 2) {
      this.message = this.domSanitizer.bypassSecurityTrustHtml(
        '<p>Ажурирање постојећих одредница још није имплементирано.</p>');
      this.display = true;
      return;
    }
    const response: any = await this.odrednicaService
      .saveOdrednica(this.makeNewDeterminant())
      .toPromise()
      .catch((error) => {
        console.log(error);
        this.message = this.domSanitizer.bypassSecurityTrustHtml(
          '<p>Није могуће додати нову одредницу. Унесите све потребне податке.</p>');
        this.display = true;
      });

    if (response) {
      this.message = this.domSanitizer.bypassSecurityTrustHtml(
        '<p>Успешно додата нова одредница.</p>');
      this.display = true;
    }
  }

  finish(): void {
    this.message = this.domSanitizer.bypassSecurityTrustHtml(
      '<p>Операција још није имплементирана.</p>');
    this.display = true;
  }

  preview(): void {
    const tekst = this.previewService.preview(this.makeNewDeterminant());
    this.message = this.domSanitizer.bypassSecurityTrustHtml(tekst);
    this.display = true;
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
          this.formMode = 1;
          this.id = null;
          this.selectedState = this.enumService.getEntryState(1);
          break;
        case 'edit':
          this.formMode = 2;
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            this.odrednicaService.getOdrednica(this.id).subscribe((value) => {
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
      varijante: this.variants.map((variant, index) => { return {
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
      version: 1, // TODO: sacuvaj prilikom edita postojece odrednice
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
              kvalifikatori: pz.qualificators.map((q, idx2) => { return {
                  redni_broj: idx2 + 1,
                  kvalifikator_id: q.id,
                  skracenica: q.abbreviation
                };
              }),
              konkordanse: pz.concordances.map((c, idx2) => { return {
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
          kvalifikatori: z.qualificators.map((q, idx) => { return {
              redni_broj: idx + 1,
              kvalifikator_id: q.id,
              skracenica: q.abbreviation
            };
          }),
          konkordanse: z.concordances.map((c, idx) => { return {
              redni_broj: idx + 1,
              opis: c.concordance,
            };
          }),
        };
      }) : [],
    };
    if (this.id !== null) {
      determinant.id = this.id;
    }
    console.log('Sastavljeno za server:', determinant);
    return determinant;
  }

  fillForm(value: any): void {
    console.log('Procitano sa servera:', value);
    this.wordE = value.rec;
    this.wordI = value.ijekavski;
    for (const v of value.varijantaodrednice_set) {
      this.variants.push({ nameE: v.tekst, nameI: v.ijekavski });
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
        expressions: z.izrazfraza_set.map((e) => { return {
          value: e.opis,
          tekst: e.tekst,
          keywords: [],
          qualificators: e.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        }; }),
        qualificators: z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
        concordances: z.konkordansa_set.map((k) => ({ concordance: k.opis })),
      };
      for (const pz of z.podznacenje_set) {
        obj.submeanings.push({
          value: pz.tekst,
          expressions: pz.izrazfraza_set.map((e, idx) => { return {
              value: e.opis,
              tekst: e.tekst,
              keywords: [],
              qualificators: pz.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
            };
          }),
          qualificators: pz.kvalifikatorpodznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
          concordances: pz.konkordansa_set.map((k) => ({ concordance: k.opis })),
        });
      }
      this.meanings.push(obj);
    }
    this.expressions = [];
    for (const expr of value.izrazfraza_set) {
      this.expressions.push({ value: expr.opis, tekst: expr.tekst, keywords: [], qualificators: expr.kvalifikatorfraze_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)) });
    }
    this.qualificators = value.kvalifikatorodrednice_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
  }

  fillTestOdrednica(): void {
    const value1 = {
      id: 42,
      rec: 'ски̏нути',
      ijekavski: null,
      vrsta: 1,
      rod: null,
      nastavak: '',
      info: 'аор. ски̏нух и ски̏дох',
      glagolski_vid: 1,
      glagolski_rod: 4,
      prezent: '-не̄м',
      broj_pregleda: 0,
      vreme_kreiranja: '2021-02-11T22:52:44.769341+01:00',
      poslednja_izmena: '2021-02-11T22:52:44.769341+01:00',
      stanje: 1,
      version: 2,
      varijantaodrednice_set: [],
      kolokacija_set: [],
      recukolokaciji_set: [],
      znacenje_set: [
        {
          id: 55,
          tekst: '',
          odrednica_id: 42,
          podznacenje_set: [
            {
              id: 36,
              tekst: 'довести са вишег на нижи положај, спустити са неког вишег места на ниже место; уклонити са нечега (обично оно што је окачено, натакнуто и сл.)',
              znacenje_id: 55,
              kvalifikatorpodznacenja_set: [],
              izrazfraza_set: [],
              konkordansa_set: [
                { redni_broj: 1, opis: '~ маче с дрвета', podznacenje_id: 36 },
                { redni_broj: 2, opis: '~ књигу с полице', podznacenje_id: 36 },
                { redni_broj: 3, opis: '~ торбу с клина', podznacenje_id: 36 },
              ],
              qualificators: []
            },
            {
              id: 37,
              tekst: 'уклонити с кога или чега оно што је око или преко њега, што га прекрива, обухвата, што служи као заштита (од хладноће нпр.) и сл.',
              znacenje_id: 55,
              kvalifikatorpodznacenja_set: [],
              izrazfraza_set: [],
              konkordansa_set: [
                { redni_broj: 1, opis: '~ кору с дрвета', podznacenje_id: 37 },
                { redni_broj: 2, opis: '~ боју с намештаја', podznacenje_id: 37 },
                { redni_broj: 3, opis: '~ шминку', podznacenje_id: 37 },
                { redni_broj: 4, opis: '~ омот', podznacenje_id: 37 },
                { redni_broj: 5, opis: '~ одећу', podznacenje_id: 37 },
                { redni_broj: 6, opis: '~ покривач', podznacenje_id: 37 },
              ],
              qualificators: []
            },
            {
              id: 38,
              tekst: 'уопште уклонити с кога или чега оно што је на њему, одн. на његовој површини',
              znacenje_id: 55,
              kvalifikatorpodznacenja_set: [],
              izrazfraza_set: [],
              konkordansa_set: [
                { redni_broj: 1, opis: '~ мрљу', podznacenje_id: 38 },
                { redni_broj: 2, opis: '~ израслину', podznacenje_id: 38 },
              ],
              qualificators: []
            }
          ],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: [],
        },
        {
          id: 56,
          tekst: 'скинути род, убрати',
          odrednica_id: 42,
          podznacenje_set: [],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        },
        {
          id: 57,
          tekst: 'искрцати, одн. истоварити са превозног средства',
          odrednica_id: 42,
          podznacenje_set: [],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        },
        {
          id: 58,
          tekst: '',
          odrednica_id: 42,
          podznacenje_set: [
            {
              id: 39,
              tekst: 'учинити да неко оде са неког положаја, да напусти неко место, неку функцију, дужност и др.',
              znacenje_id: 58,
              kvalifikatorpodznacenja_set: [],
              izrazfraza_set: [],
              konkordansa_set: [],
              qualificators: []
            },
            {
              id: 40,
              tekst: 'оборити метком, устрелити; погодити',
              znacenje_id: 58,
              kvalifikatorpodznacenja_set: [],
              izrazfraza_set: [],
              konkordansa_set: [],
              qualificators: []
            }
          ],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        },
        {
          id: 59,
          tekst: 'прекинути важење неког ограничења (санкције)',
          odrednica_id: 42,
          podznacenje_set: [],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        },
        {
          id: 60,
          tekst: 'узети, преузети са узорка, снимити, копирати',
          odrednica_id: 42,
          podznacenje_set: [],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        },
        {
          id: 61,
          tekst: 'лишити одеће, свући',
          odrednica_id: 42,
          podznacenje_set: [],
          kvalifikatorznacenja_set: [],
          izrazfraza_set: [],
          konkordansa_set: []
        }
      ],
      izrazfraza_set: [
        {
          id: 18,
          opis: 'престати узимати дрогу, престати бити наркоман',
          tekst: '~ се с дроге',
          redni_broj: 1,
          odrednica_id: 42,
          znacenje_id: null,
          podznacenje_id: null,
          kvalifikatorfraze_set: []
        }
      ],
      kvalifikatorodrednice_set: [],
      izmenaodrednice_set: [
        {
          id: 15,
          odrednica_id: 42,
          operacija_izmene_id: 18,
          user_id: 1,
          vreme: '2021-02-11T22:52:44.769341+01:00'
        }
      ],
      opciono_se: null
    };
    this.fillForm(value1);
  }
}

import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Glagol } from '../../models/glagol';
import { GlagolOblik } from '../../models/glagolOblik';
import { GlagolVarijanta } from '../../models/glagolVarijanta';
import { GlagolService } from '../../services/glagol/glagol.service';

interface Vid {
  id: number;
  name: string;
}

interface Rod {
  id: number;
  name: string;
}

interface VarijantaHTML {
  vreme: number;
  lice: string;
  value: string;
}

@Component({
  selector: 'glagol',
  templateUrl: './glagol.component.html',
  styleUrls: ['./glagol.component.scss']
})
export class GlagolComponent implements OnInit {

  @Input() glagol: Glagol;

  @Output() glagolChanged: EventEmitter<Glagol> = new EventEmitter();

  vidovi: Vid[];
  selectedVid: Vid;
  rodovi: Rod[];
  selectedRod: Rod;
  variants: GlagolVarijanta[];
  variantsHTML: VarijantaHTML[];
  variantsMap: any;
  id: number;
  vreme: number;
  licaList: any[];

  constructor(private messageService: MessageService, private glagolService: GlagolService, private route: ActivatedRoute) {
    this.vidovi = [
      { id: 1, name: 'свршени' },
      { id: 2, name: 'несвршени' },
      { id: 3, name: 'двовидски' }
    ];
    this.selectedVid = { id: 0, name: '' };
    this.rodovi = [
      { id: 1, name: 'прелазни' },
      { id: 2, name: 'непрелазни' },
      { id: 3, name: 'повратни' },
      { id: 4, name: 'медијални' }
    ];
    this.selectedRod = { id: 0, name: '' };
    this.variantsMap = {
      'pr.l.jed.': 'jd1',
      'dr.l.jed.': 'jd2',
      'tr.l.jed.': 'jd3',
      'pr.l.mn.': 'mn1',
      'dr.l.mn.': 'mn2',
      'tr.l.mn.': 'mn3'
    };
    this.variantsHTML = new Array<VarijantaHTML>();
    this.vreme = 1;
    this.licaList = [
      { name: 'pr.l.jed.', value: 'jd1' },
      { name: 'dr.l.jed.', value: 'jd2' },
      { name: 'tr.l.jed.', value: 'jd3' },
      { name: 'pr.l.mn.', value: 'mn1' },
      { name: 'dr.l.mn.', value: 'mn2' },
      { name: 'tr.l.mn.', value: 'mn3' }
    ];
  }

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.glagol = {
        infinitiv: '',
        vid: 0,
        rod: 0,
        rgp_mj: '',
        rgp_zj: '',
        rgp_sj: '',
        rgp_mm: '',
        rgp_zm: '',
        rgp_sm: '',
        gpp: '',
        gps: '',
        oblici: this.makeOblici(),
        varijante: new Array<GlagolVarijanta>()
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getGlagolById();
      this.glagol = { // test case, delete if getting data from the server
        id: this.id,
        infinitiv: 'тестирати',
        vid: 2,
        rod: 3,
        rgp_mj: 'тестирао',
        rgp_zj: 'тестирала',
        rgp_sj: 'тестирало',
        rgp_mm: 'тестирали',
        rgp_zm: 'тестирале',
        rgp_sm: 'тестирала',
        gpp: 'тестиравши',
        gps: 'тестирајући',
        version: 1,
        oblici: [
          { vreme:1, jd1:'тестирам', jd2:'тестираш', jd3:'тестира', mn1:'тестирамо', mn2:'тестирате', mn3:'тестирају' },
          { vreme:2, jd1:'тестираћу', jd2:'тестираћеш', jd3:'тестираће', mn1:'тестираћемо', mn2:'тестираћете', mn3:'тестираће' },
          { vreme:3, jd1:'тестирах', jd2:'тестира', jd3:'тестира', mn1:'тестирасмо', mn2:'тестирасте', mn3:'тестираше' },
          { vreme:4, jd1:'тестирах', jd2:'тестираше', jd3:'тестираше', mn1:'тестирасмо', mn2:'тестирасте', mn3:'тестираху' },
          { vreme:5, jd1:'', jd2:'тестирај', jd3:'', mn1:'тестирајмо', mn2:'тестирајте', mn3:'' }
        ],
        varijante: [
          {
            id: 1,
            glagol_id: this.id,
            redni_broj: 1,
            vreme: 1,
            jd1: 'пробам',
            jd2: 'пробаш',
            jd3: 'проба',
            mn1: '',
            mn2: '',
            mn3: ''
          }
        ]
      };
      this.handlePovratniGlagol();
      this.removeVariantProperties();
      this.loadHTMLVariants();
      this.selectedVid = this.vidovi.find(vid => vid.id === this.glagol.vid);
      this.selectedRod = this.rodovi.find(rod => rod.id === this.glagol.rod);
    }
  }

  changeGlagol(): void {
    this.glagol.vid = this.selectedVid.id;
    this.glagol.rod = this.selectedRod.id;
    if (this.variantsHTML.length > 0)
      this.setGlagolVarijante();
    this.glagolChanged.emit(this.glagol);
  }

  async getGlagolById() {
    const response: any = await this.glagolService.getGlagol(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражени глагол није пронађен'});
      });
    if (response) {
      this.glagol = response.map((item: Glagol) => {
        return {
          infinitiv: item.infinitiv, vid: item.vid, rod: item.rod,
          rgp_mj: item.rgp_mj, rgp_zj: item.rgp_zj, rgp_sj: item.rgp_sj,
          rgp_mm: item.rgp_mm, rgp_zm: item.rgp_zm, rgp_sm: item.rgp_sm,
          gpp: item.gpp, gps: item.gps, version: item.version,
          id: item.id, oblici: item.oblikglagola_set, varijante: item.varijantaglagola_set
        };
      });
      if (this.glagol.rod == 3)
        this.handlePovratniGlagol();
    }
  }

  handlePovratniGlagol(): void {
    let keys = ['infinitiv', 'rgp_mj', 'rgp_zj', 'rgp_sj', 'rgp_mm', 'rgp_zm', 'rgp_sm', 'gpp', 'gps'];
    for (const key in this.glagol)
      if (keys.includes(key) && this.glagol[key].endsWith(' се'))
        this.glagol[key] = this.glagol[key].replace(' се', '');
    for (let i=0; i<this.glagol.oblici.length; i++)
      for (const key in this.glagol.oblici[i])
        if (key !== 'vreme' && this.glagol.oblici[i][key].endsWith(' се'))
          this.glagol.oblici[i][key] = this.glagol.oblici[i][key].replace(' се', '');
    keys = ['jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3'];
    for (let i=0; i<this.glagol.varijante.length; i++)
      for (const key in this.glagol.varijante[i])
        if (keys.includes(key) && this.glagol.varijante[i][key].endsWith(' се'))
          this.glagol.varijante[i][key] = this.glagol.varijante[i][key].replace(' се', '');
  }

  makeOblici(): GlagolOblik[] {
    return [
        { vreme:1, jd1:'', jd2:'', jd3:'', mn1:'', mn2:'', mn3:'' },
        { vreme:2, jd1:'', jd2:'', jd3:'', mn1:'', mn2:'', mn3:'' },
        { vreme:3, jd1:'', jd2:'', jd3:'', mn1:'', mn2:'', mn3:'' },
        { vreme:4, jd1:'', jd2:'', jd3:'', mn1:'', mn2:'', mn3:'' },
        { vreme:5, jd1:'', jd2:'', jd3:'', mn1:'', mn2:'', mn3:'' }
    ];
  }

  addVariant(): void {
    this.variantsHTML.push(
      { vreme: this.vreme, lice: 'jd1', value: '' }
    );
  }

  removeVariant(variant: VarijantaHTML): void {
    this.variantsHTML.splice(this.variantsHTML.indexOf(variant), 1);
    let glagolVar = this.glagol.varijante.find(v => v.vreme === variant.vreme);
    for (const key in glagolVar)
      if (key !== 'vreme')
        glagolVar[key] = '';
    this.changeGlagol();
  }

  loadHTMLVariants(): void {
    let keys = ['jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3'];
    for (let i=0; i<this.glagol.varijante.length; i++)
      for (const key in this.glagol.varijante[i])
        if (keys.includes(key) && this.glagol.varijante[i][key] !== '') {
          this.variantsHTML.push(
            { vreme: this.glagol.varijante[i].vreme, lice: key, value: this.glagol.varijante[i][key] }
          );
        }
  }

  setGlagolVarijante(): void {
    this.clearGlagolVarijante();
    for (let i=1; i<6; i++) { // vremena
      let variant: any;
      for (let j=0; j<this.variantsHTML.length; j++) {
        if (this.variantsHTML[j].vreme === i) {
          variant = this.glagol.varijante.find(v => v.vreme === i);
          if (variant)
            variant[this.variantsHTML[j].lice] = this.variantsHTML[j].value;
          else {
            this.glagol.varijante.push(
              {
                vreme: this.vreme,
                jd1: this.variantsHTML[j].lice === 'jd1' ? this.variantsHTML[j].value : '',
                jd2: this.variantsHTML[j].lice === 'jd2' ? this.variantsHTML[j].value : '',
                jd3: this.variantsHTML[j].lice === 'jd3' ? this.variantsHTML[j].value : '',
                mn1: this.variantsHTML[j].lice === 'mn1' ? this.variantsHTML[j].value : '',
                mn2: this.variantsHTML[j].lice === 'mn2' ? this.variantsHTML[j].value : '',
                mn3: this.variantsHTML[j].lice === 'mn3' ? this.variantsHTML[j].value : '',
              }
            );
          }
        }
      }
    }
  }

  clearGlagolVarijante(): void {
    for (let i=0; i<this.glagol.varijante.length; i++)
      for (const key in this.glagol.varijante[i])
        if (key !== 'vreme')
          this.glagol.varijante[i][key] = '';
  }

  removeVariantProperties(): void {
    for (let i=0; i<this.glagol.varijante.length; i++) {
      if (this.glagol.varijante[i].glagol_id)
        delete this.glagol.varijante[i].glagol_id;
      if (this.glagol.varijante[i].id)
        delete this.glagol.varijante[i].id;
      if (this.glagol.varijante[i].redni_broj)
        delete this.glagol.varijante[i].redni_broj;
    }
  }

  setVreme(e: any) {
    this.vreme = e.index + 1;
  }
}

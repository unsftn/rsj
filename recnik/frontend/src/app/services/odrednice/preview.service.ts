import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class PreviewService {
  rod = { 1: 'м', 2: 'ж', 3: 'с' };
  gvid = { 1: 'свр.', 2: 'несвр.', 3: 'свр. и несвр.' };
  azbuka = 'абвгдђежзијклљмнњопрстћуфхцчџш';
  constructor() { }

  preview(odrednica): string {
    let tekst = `<div class="odrednica"><b>${odrednica.rec}</b>`;
    if (odrednica.vrsta === 1 && odrednica.opciono_se) {
      tekst = `<div class="odrednica"><b>${odrednica.rec} (се)</b>`;
    }
    if (odrednica.varijante.length > 0) {
      tekst += ` (${odrednica.varijante.map(v => v.tekst).join(', ')})`;
    }
    switch (odrednica.vrsta) {
      case 0: // imenica
        if (odrednica.nastavak) {
          tekst += `, ${odrednica.nastavak}`;
        }
        tekst += ` <small>${this.rod[odrednica.rod]}</small> `;
        if (odrednica.info) {
          tekst += `(${odrednica.info}) `;
        }
        break;
      case 1: // glagol
        if (odrednica.prezent) {
          tekst += `, ${odrednica.prezent} `;
        }
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        if (odrednica.glagolski_vid > 0) {
          tekst += `<small>${this.gvid[odrednica.glagolski_vid]}</small> `;
        }
        break;
      case 2: // pridev
        if (odrednica.nastavak) {
          tekst += `, ${odrednica.nastavak}`;
        }
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        break;
      case 3: // prilog
        tekst += ` <small>прил.</small> `;
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        break;
      case 4: //
        // TODO
        break;
      case 5: //
        // TODO
        break;
      case 6: // uzvik
        tekst += ` <small>узв.</small> `;
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        break;
      case 7: // recca
        tekst += ` <small>речца</small> `;
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        break;
      case 8: // veznik
        tekst += ` <small>везн.</small> `;
        if (odrednica.info) {
          tekst += ` (${odrednica.info}) `;
        }
        break;
      case 9: // broj
        break;
    }
    if (odrednica.kvalifikatori.length > 0) {
      tekst += this.render_kvalifikatori(odrednica.kvalifikatori);
    }
    if (odrednica.znacenja.length === 1) {
      tekst += this.render_znacenje(odrednica.znacenja[0]);
    } else {
      odrednica.znacenja.filter(z => !z.znacenje_se).forEach((z, i) => {
        tekst += ` <b>${i + 1}.</b> ${this.render_znacenje(z)}`;
      });
      const znacenja2 = odrednica.znacenja.filter(z => z.znacenje_se);
      if (znacenja2.length > 0) {
        tekst += ' <b>&#9632; ~ се</b> ';
        znacenja2.forEach((z, i) => {
          tekst += ` <b>${i + 1}.</b> ${this.render_znacenje(z)}`;
        });
      }
    }
    tekst += this.render_izrazi_fraze_odrednice(odrednica.izrazi_fraze);
    return `${this.tacka(tekst)}</div>`;
  }

  render_znacenje(znacenje: any): string {
    let tekst = '';
    if (znacenje.kvalifikatori.length > 0) {
      tekst += this.render_kvalifikatori(znacenje.kvalifikatori);
    }
    tekst += `${this.tacka(znacenje.tekst)}`;
    if (znacenje.konkordanse.length > 0) {
      tekst = this.dvotacka(tekst);
      tekst += this.render_konkordanse(znacenje.konkordanse);
    }
    tekst += this.render_izrazi_fraze_znacenja(znacenje.izrazi_fraze);
    znacenje.podznacenja.forEach((value, index) => {
      tekst += ` <b>${this.azbuka.charAt(index)}.</b> ${this.render_podznacenje(value)}`;
    });
    return tekst;
  }

  render_podznacenje(podznacenje: any): string {
    let tekst = '';
    if (podznacenje.kvalifikatori.length > 0) {
      tekst += this.render_kvalifikatori(podznacenje.kvalifikatori);
    }
    tekst += `${this.tacka(podznacenje.tekst)}`;
    if (podznacenje.konkordanse.length > 0) {
      tekst = this.dvotacka(tekst);
      tekst += this.render_konkordanse(podznacenje.konkordanse);
    }
    tekst += this.render_izrazi_fraze_znacenja(podznacenje.izrazi_fraze);
    return tekst;
  }

  render_izrazi_fraze_znacenja(izraziFraze: any[]): string {
    let tekst = '';
    izraziFraze.forEach((value) => {
      tekst += ` &#8212; <i>${this.tacka(value.opis)}</i>`;
    });
    return tekst;
  }

  render_izrazi_fraze_odrednice(izraziFraze: any[]): string {
    let tekst = '';
    izraziFraze.forEach((value) => {
      tekst += ` &bull; <small><b>${value.tekst}</b></small> `;
      tekst += this.render_kvalifikatori(value.kvalifikatori);
      tekst += ` <i>${this.tacka(value.opis)}</i>`;
    });
    return tekst;
  }

  render_kvalifikatori(kvali: any[]): string {
    let tekst = '';
    kvali.forEach((value) => {
      tekst += ` <small>${this.tacka(value.skracenica)}</small> `;
    });
    return tekst;
  }

  render_konkordanse(konkordanse: any[]): string {
    return this.tacka(konkordanse.map(v => `<i>${v.opis}</i>`).join(', '));
  }

  tacka(tekst: string): string {
    if (tekst.length === 0) {
      return tekst;
    }
    const regex = new RegExp('[.,:!?>]$');
    if (!regex.test(tekst)) {
      return tekst + '.';
    }
    return tekst;
  }

  dvotacka(tekst: string): string {
    if (tekst.length === 0) {
      return tekst;
    }
    if (tekst[tekst.length - 1] === '.') {
      return tekst.substring(0, tekst.length - 1) + ': ';
    }
    return tekst + ': ';
  }
}

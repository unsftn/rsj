import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class PreviewService {
  rod = { 1: 'м', 2: 'ж', 3: 'с' };
  gvid = { 1: 'свр.', 2: 'несвр.', 3: 'двовид.' };
  azbuka = 'абвгдђежзијклљмнњопрстћуфхцчџш';
  constructor() { }

  preview(odrednica): string {
    let tekst = `<div class="odrednica"><b>${odrednica.rec}</b>`;
    if (odrednica.varijante.length > 0) {
      tekst += ` (${odrednica.varijante.join(', ')})`;
    }
    switch (odrednica.vrsta) {
      case 0: // imenica
        console.log('Rod', odrednica.rod);
        tekst += ` <small>${this.rod[odrednica.rod]}</small>`;
        break;
      case 1: // glagol
        if (odrednica.nastavak) {
          tekst += `, ${odrednica.nastavak}`;
        }
        if (odrednica.prezent) {
          tekst += `, ${odrednica.prezent}`;
        }
        if (odrednica.glagolski_vid > 0) {
          tekst += `, <small>${this.gvid[odrednica.glagolski_vid]}</small>`;
        }
        break;
      case 2: // pridev
        if (odrednica.nastavak) {
          tekst += `, ${odrednica.nastavak}`;
        }
        break;
      case 3: // prilog
        tekst += ` <small>прил.</small> `;
        break;
      case 4: //
        // TODO
        break;
      case 5: //
        // TODO
        break;
      case 6: // uzvik
        tekst += ` <small>узв.</small> `;
        break;
      case 7: // recca
        tekst += ` <small>речца</small> `;
        break;
      case 8: // veznik
        tekst += ` <small>везн.</small> `;
        break;
      case 9: // broj
        break;
    }
    if (odrednica.kvalifikatori.length > 0)
      tekst += this.render_kvalifikatori(odrednica.kvalifikatori);
    if (odrednica.znacenja.length === 1) {
      tekst += this.render_znacenje(odrednica.znacenja[0]);
    } else {
      odrednica.znacenja.forEach((z, i) => {
        tekst += ` <b>${i + 1}.</b> ${this.render_znacenje(z)}`;
      });
    }
    return `${tekst}</div>`;
  }

  render_znacenje(znacenje: any): string {
    let tekst = '';
    if (znacenje.kvalifikatori.length > 0)
      tekst += this.render_kvalifikatori(znacenje.kvalifikatori);
    tekst += `${this.tacka(znacenje.tekst)}`;
    tekst += this.render_izrazi_fraze(znacenje.izrazi_fraze);
    znacenje.podznacenja.forEach((value, index) => {
      tekst += ` <b>${this.azbuka.charAt(index)}.</b> ${this.render_podznacenje(value)}`;
    });
    return tekst;
  }

  render_podznacenje(podznacenje: any): string {
    let tekst = '';
    if (podznacenje.kvalifikatori.length > 0)
      tekst += this.render_kvalifikatori(podznacenje.kvalifikatori);
    tekst += `${this.tacka(podznacenje.tekst)}`;
    tekst += this.render_izrazi_fraze(podznacenje.izrazi_fraze);
    return tekst;
  }

  render_izrazi_fraze(izraziFraze: any[]): string {
    let tekst = '';
    izraziFraze.forEach((value) => {
      tekst += ` &#8212; <i>${this.tacka(value.opis)}</i>`;
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

  tacka(tekst: string): string {
    if (tekst.length === 0) {
      return tekst;
    }
    const regex = new RegExp('[.,:!?]$');
    if (!regex.test(tekst)) {
      return tekst + '.';
    }
    return tekst;
  }
}

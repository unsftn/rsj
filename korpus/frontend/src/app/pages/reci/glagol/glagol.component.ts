import { Component, OnInit, AfterViewInit, ViewChild, ElementRef} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { Glagol, GlagolskaVarijanta, GlagolskiRod, GlagolskiVid, toGlagol } from '../../../models/reci';
import { GlagolService } from '../../../services/reci';
import { SearchService } from '../../../services/search';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-glagol',
  templateUrl: './glagol.component.html',
  styleUrls: ['./glagol.component.scss']
})
export class GlagolComponent implements OnInit, AfterViewInit {

  glagol: Glagol;

  id: number;
  editMode: boolean;
  rodovi: GlagolskiRod[];
  vidovi: GlagolskiVid[];
  varijante: GlagolskaVarijanta[];
  showDupes: boolean;
  dupes: any[];
  @ViewChild('infinitiv') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private glagolService: GlagolService,
    private searchService: SearchService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Глагол');
    this.initNew();
    this.rodovi = this.glagolService.getRodovi();
    this.vidovi = this.glagolService.getVidovi();
    this.varijante = this.glagolService.getVarijante();
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.load();
            });
          break;
      }
    });
  }

  ngAfterViewInit(): void {
    this.textInput.nativeElement.focus();
  }

  initNew(): void {
    this.glagol = this.glagolService.new();
  }

  addVarijanta(index: number): void {
    this.glagol.oblici[index].varijante.push({varijanta: null, tekst: ''});
  }

  moveUp(vreme: number, index: number): void {
    if (index === 0)
      return;
    const temp = this.glagol.oblici[vreme].varijante.splice(index, 1)[0];
    this.glagol.oblici[vreme].varijante.splice(index - 1, 0, temp);
  }

  moveDown(vreme: number, index: number): void {
    if (index === this.glagol.oblici[vreme].varijante.length - 1)
      return;
    const temp = this.glagol.oblici[vreme].varijante.splice(index, 1)[0];
    this.glagol.oblici[vreme].varijante.splice(index + 1, 0, temp);
  }

  remove(vreme: number, index: number): void {
    this.glagol.oblici[vreme].varijante.splice(index, 1);
  }

  assert(condition: boolean, message: string): void {
    if (condition) {
      this.messageService.add({
        severity: 'error',
        summary: 'Грешка',
        life: 0,
        detail: message,
      });
      throw new Error();
    }
  }

  check(): boolean {
    try {
      for (const oblik of this.glagol.oblici)
        for (const v of oblik.varijante) {
          this.assert(v.varijanta === null || v.tekst.trim() === '', 'Бар једна варијанта није попуњена.');
        }
      this.assert(this.glagol.infinitiv.trim() === '', 'Инфинитив мора бити попуњен!');
      return true;
    } catch (e) {
      return false;
    }
  }

  load(): void {
    this.glagolService.get(this.id).subscribe({
      next: (item) => {
        this.glagol = toGlagol(item);
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Глагол није учитан',
        });
        this.router.navigate(['/']);
      }
    });
  }

  save(): void {
    console.log('Snimanje glagola:', this.glagol);
    if (!this.editMode) {
      this.glagolService.add(this.glagol).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Глагол је успешно сачуван.`,
          });
          this.router.navigate(['/glagol', data.id]);
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    } else {
      this.glagolService.update(this.glagol).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Глагол је успешно сачуван.`,
          });
          this.load();
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    }
  }

  saveAvailable() {
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.isEditor())
      return true;
    // dobrovoljci mogu da menjaju samo reci ciji vlasnik je WikiMorph
    if (this.tokenStorageService.isVolunteer() && this.glagol.vlasnik.id === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.glagol.vlasnik.id)
      return true;
    return false;
  }

  vlasnikImePrezime(): string {
    if (!this.glagol.vlasnik)
      return '';
    return (this.glagol.vlasnik.first_name + ' ' + this.glagol.vlasnik.last_name).trim();
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.glagol.infinitiv, this.id).subscribe({
      next: (data) => {
        if (data.length > 0) {
          this.dupes = data;
          this.showDupes = true;
        } else {
          this.dupes = [];
          this.showDupes = false;
          this.save();
        }
      },
      error: (error) => console.log(error),
    });
  }

  dupesYes(): void {
    this.showDupes = false;
    this.save();
  }

  dupesNo(): void {
    this.showDupes = false;
  }
}

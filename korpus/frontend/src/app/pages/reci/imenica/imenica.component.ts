import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { Imenica, toImenica, VrstaImenice } from '../../../models/reci';
import { ImenicaService, RecService } from '../../../services/reci';
import { SearchService } from '../../../services/search';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-imenica',
  templateUrl: './imenica.component.html',
  styleUrls: ['./imenica.component.scss']
})
export class ImenicaComponent implements OnInit, AfterViewInit {

  imenica: Imenica;

  id: number;
  editMode: boolean;
  vrste: VrstaImenice[];
  returnUrl: string;
  sourceWord: string;
  showDupes: boolean;
  showAreYouSure: boolean;
  dupes: any[];
  dirty: boolean;
  @ViewChild('nomjed') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private imenicaService: ImenicaService,
    private searchService: SearchService,
    private recService: RecService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Именица');
    this.initNew();
    this.vrste = this.imenicaService.getVrste();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
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
    this.imenica = this.imenicaService.new();
  }

  check(): boolean {
    try {
      this.assert(this.imenica.nomjed.trim().length === 0 && this.imenica.nommno.trim().length === 0, 'Мора се унети номинатив једнине или множине.');
      return true;
    } catch (e) {
      return false;
    }
  }

  addVarijanta(): void {
    const rbr = this.imenica.varijante.length;
    this.imenica.varijante.push({ redni_broj: rbr + 1, nomjed: '', genjed: '', datjed: '', akujed: '', vokjed: '', insjed: '', lokjed: '', nommno: '', genmno: '', datmno: '', akumno: '', vokmno: '', insmno: '', lokmno: ''});
    setTimeout(() => {
      document.getElementById(`nomjed${this.imenica.varijante.length - 1}`).focus();
      scrollTo(0, document.body.scrollHeight);
    });
  }

  load(): void {
    this.imenicaService.get(this.id).subscribe({
      next: (item) => {
        this.imenica = toImenica(item);
        this.dirty = false;
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Именица није учитана',
        });
        this.router.navigate(['/']);
      }
    });
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

  vlasnikImePrezime(): string {
    if (!this.imenica.vlasnik)
      return '';
    return (this.imenica.vlasnik.first_name + ' ' + this.imenica.vlasnik.last_name).trim();
  }

  save(): void {
    console.log('Snimanje imenice:', this.imenica);
    if (!this.editMode) {
      this.imenicaService.add(this.imenica).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Именица је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/imenica', data.id]);
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
      this.imenicaService.update(this.imenica).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Именица је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
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

  moveUp(index: number): void {
    if (index === 0)
      return;
    const temp = this.imenica.varijante.splice(index, 1)[0];
    this.imenica.varijante.splice(index - 1, 0, temp);
  }

  moveDown(index: number): void {
    if (index === this.imenica.varijante.length - 1)
      return;
    const temp = this.imenica.varijante.splice(index, 1)[0];
    this.imenica.varijante.splice(index + 1, 0, temp);
  }

  remove(index: number): void {
    this.imenica.varijante.splice(index, 1);
  }

  saveAvailable() {
    if (!this.dirty)
      return false;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.isEditor())
      return true;
    // dobrovoljci mogu da menjaju samo reci ciji vlasnik je WikiMorph
    if (this.tokenStorageService.isVolunteer() && this.imenica.vlasnikID === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.imenica.vlasnikID)
      return true;
    return false;
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.imenica.nomjed, this.id).subscribe({
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

  setDirty(): void {
    this.dirty = true;
  }

  isAdmin(): boolean {
    return this.tokenStorageService.isAdmin();
  }

  areYouSure(): void {
    this.showAreYouSure = true;
  }

  sureNo(): void {
    this.showAreYouSure = false;
  }

  sureYes(): void {
    this.showAreYouSure = false;
    this.removeWord();
  }

  removeWord(): void {
    this.recService.remove(this.id, 0).subscribe({
      next: (data) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Успех',
          life: 3000,
          detail: `Реч је успешно обрисана.`,
        });
        this.router.navigate(['/']);
      },
      error: (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: `Неуспешно брисање: ${error}`,
        });
      }
    });
  }
}

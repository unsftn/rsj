import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { RecService, UzvikService } from '../../../services/reci/';
import { SearchService } from '../../../services/search';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { Uzvik, toUzvik } from '../../../models/reci';

@Component({
  selector: 'app-uzvik',
  templateUrl: './uzvik.component.html',
  styleUrls: ['./uzvik.component.scss']
})
export class UzvikComponent implements OnInit, AfterViewInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  uzvik: Uzvik;
  showDupes: boolean;
  showAreYouSure: boolean;
  dupes: any[];
  dirty: boolean;
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private uzvikService: UzvikService,
    private searchService: SearchService,
    private recService: RecService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Узвик');
    this.uzvik = this.uzvikService.new();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.uzvik = { tekst: '', vlasnikID: this.tokenStorageService.getUser().id };
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

  check(): boolean {
    try {
      this.assert(this.uzvik.tekst.trim().length === 0, 'Мора се унети садржај.');
      return true;
    } catch (e) {
      return false;
    }
  }

  load(): void {
    this.uzvikService.get(this.id).subscribe({
      next: (item) => {
        this.uzvik = toUzvik(item);
        this.dirty = false;
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: `Узвик није учитан: ${error}`,
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

  save(): void {
    if (this.editMode) {
      this.uzvikService.update({id: this.id, tekst: this.uzvik.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Узвик је успешно сачуван.`,
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
    } else {
      this.uzvikService.add({tekst: this.uzvik.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Узвик је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/uzvik', data.id]);
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
    if (!this.dirty)
      return false;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.isEditor())
      return true;
    // dobrovoljci mogu da menjaju samo reci ciji vlasnik je WikiMorph
    if (this.tokenStorageService.isVolunteer() && this.uzvik.vlasnikID === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.uzvik?.vlasnikID)
      return true;
    return false;
  }

  vlasnikImePrezime(): string {
    if (!this.uzvik.vlasnik)
      return '';
    return (this.uzvik.vlasnik.first_name + ' ' + this.uzvik.vlasnik.last_name).trim();
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.uzvik.tekst, this.id).subscribe({
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
    this.recService.remove(this.id, 6).subscribe({
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

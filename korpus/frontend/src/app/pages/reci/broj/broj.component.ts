import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { Broj, toBroj } from '../../../models/reci';
import { BrojService } from '../../../services/reci';
import { SearchService } from '../../../services/search';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-broj',
  templateUrl: './broj.component.html',
  styleUrls: ['./broj.component.scss']
})
export class BrojComponent implements OnInit, AfterViewInit {

  broj: Broj;
  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  showDupes: boolean;
  dupes: any[];
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private brojService: BrojService,
    private searchService: SearchService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Број');
    this.showDupes = false;
    this.dupes = [];
    this.initNew();
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
              this.brojService.get(this.id).subscribe((item) => {
                this.broj = toBroj(item);
              },
              (error) => {
                console.log(error);
                this.messageService.add({
                  severity: 'error',
                  summary: 'Грешка',
                  life: 5000,
                  detail: 'Број није учитан',
                });
                this.router.navigate(['/']);
              });
            });
          break;
      }
    });
  }

  ngAfterViewInit(): void {
    this.textInput.nativeElement.focus();
  }

  initNew(): void {
    this.broj = this.brojService.new();
  }

  check(): boolean {
    try {
      this.assert(this.broj.nomjed.trim().length === 0, 'Мора се унети номинатив једнине.');
      return true;
    } catch (e) {
      return false;
    }
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
    console.log('Snimanje broja:', this.broj);
    if (!this.editMode) {
      this.brojService.add(this.broj).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Број је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/broj', data.id]);
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
      this.brojService.update(this.broj).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Број је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
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
    if (this.tokenStorageService.isVolunteer() && this.broj.vlasnikID === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.broj.vlasnikID)
      return true;
    return false;
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.broj.nomjed, this.id).subscribe({
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

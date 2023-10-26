import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { PredlogService } from '../../../services/reci/';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { SearchService } from '../../../services/search';
import { Predlog, toPredlog } from '../../../models/reci';

@Component({
  selector: 'app-predlog',
  templateUrl: './predlog.component.html',
  styleUrls: ['./predlog.component.scss']
})
export class PredlogComponent implements OnInit, AfterViewInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  predlog: Predlog;
  showDupes: boolean;
  dupes: any[];
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private predlogService: PredlogService,
    private searchService: SearchService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Предлог');
    this.predlog = this.predlogService.new();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.predlog = { tekst: '', vlasnikID: this.tokenStorageService.getUser().id };
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
      this.assert(this.predlog.tekst.trim().length === 0, 'Мора се унети садржај.');
      return true;
    } catch (e) {
      return false;
    }
  }

  load(): void {
    this.predlogService.get(this.id).subscribe({
      next: (item) => {
        this.predlog = toPredlog(item);
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: `Предлог није учитан: ${error}`,
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
      this.predlogService.update({id: this.id, tekst: this.predlog.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Предлог је успешно сачуван.`,
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
    } else {
      this.predlogService.add({tekst: this.predlog.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Предлог је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/predlog', data.id]);
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

  vlasnikImePrezime(): string {
    if (!this.predlog.vlasnik)
      return '';
    return (this.predlog.vlasnik.first_name + ' ' + this.predlog.vlasnik.last_name).trim();
  }

  saveAvailable() {
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.isEditor())
      return true;
    // dobrovoljci mogu da menjaju samo reci ciji vlasnik je WikiMorph
    if (this.tokenStorageService.isVolunteer() && this.predlog.vlasnikID === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.predlog?.vlasnikID)
      return true;
    return false;
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.predlog.tekst, this.id).subscribe({
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

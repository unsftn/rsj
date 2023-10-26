import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { Prilog, toPrilog } from '../../../models/reci';
import { PrilogService } from '../../../services/reci';
import { SearchService } from '../../../services/search';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-prilog',
  templateUrl: './prilog.component.html',
  styleUrls: ['./prilog.component.scss']
})
export class PrilogComponent implements OnInit, AfterViewInit {

  prilog: Prilog;
  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  showDupes: boolean;
  dupes: any[];
  @ViewChild('pozitiv') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private prilogService: PrilogService,
    private searchService: SearchService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Прилог');
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
    this.prilog = this.prilogService.new();
  }

  check(): boolean {
    try {
      this.assert(this.prilog.pozitiv.trim().length === 0, 'Мора се унети позитив.');
      return true;
    } catch (e) {
      return false;
    }
  }

  load(): void {
    this.prilogService.get(this.id).subscribe({
      next: (item) => {
        this.prilog = toPrilog(item);
      },
      error: (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Прилог није учитан',
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
    console.log('Snimanje priloga:', this.prilog);
    if (!this.editMode) {
      this.prilogService.add(this.prilog).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Прилог је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/prilog', data.id]);
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
      this.prilogService.update(this.prilog).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Прилог је успешно сачуван.`,
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
    if (this.tokenStorageService.isVolunteer() && this.prilog.vlasnikID === 3)
      return true;
    if (this.tokenStorageService.getUser().id === this.prilog?.vlasnikID)
      return true;
    return false;
  }

  vlasnikImePrezime(): string {
    if (!this.prilog.vlasnik)
      return '';
    return (this.prilog.vlasnik.first_name + ' ' + this.prilog.vlasnik.last_name).trim();
  }

  checkDupes(): void {
    if (!this.check()) return;
    this.searchService.checkDupes(this.prilog.pozitiv, this.id).subscribe({
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

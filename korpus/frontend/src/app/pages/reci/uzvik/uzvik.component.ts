import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { UzvikService } from '../../../services/reci/';
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
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private uzvikService: UzvikService,
  ) { }

  ngOnInit(): void {
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
              this.uzvikService.get(this.id).subscribe({
                next: (item) => {
                  this.uzvik = toUzvik(item);
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
          });
          break;        
      }
    });
  }

  ngAfterViewInit(): void {
    this.textInput.nativeElement.focus();
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
    if (this.tokenStorageService.isEditor())
      return true;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.getUser().id === this.uzvik?.vlasnikID)
      return true;
    return false;
  }
}

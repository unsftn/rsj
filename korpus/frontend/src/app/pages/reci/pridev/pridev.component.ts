import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PridevService } from 'src/app/services/reci/pridev.service';
import { Pridev, toPridev } from '../../../models/reci';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-pridev',
  templateUrl: './pridev.component.html',
  styleUrls: ['./pridev.component.scss']
})
export class PridevComponent implements OnInit, AfterViewInit {

  pridev: Pridev;

  id: number;
  editMode: boolean;
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private pridevService: PridevService,
  ) { }

  ngOnInit(): void {
    this.initNew();
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
              this.pridevService.get(this.id).subscribe({
                  next: (item) => {
                  this.pridev = toPridev(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: 'Придев није учитан',
                  });
                  this.router.navigate(['/']);
              }});
            });
          break;
      }
    });
  }

  ngAfterViewInit(): void {
    this.textInput.nativeElement.focus();
  }

  initNew(): void {
    this.pridev = this.pridevService.new();
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

  allEmpty(): boolean {
    const properties = [ 
      'mnomjed', 'mgenjed', 'mdatjed', 'makujed', 'mvokjed', 'minsjed', 'mlokjed', 'mnommno', 'mgenmno', 'mdatmno', 'makumno', 'mvokmno',
      'minsmno', 'mlokmno', 'znomjed', 'zgenjed', 'zdatjed', 'zakujed', 'zvokjed', 'zinsjed', 'zlokjed', 'znommno', 'zgenmno', 'zdatmno',
      'zakumno', 'zvokmno', 'zinsmno', 'zlokmno', 'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed', 'snommno',
      'sgenmno', 'sdatmno', 'sakumno', 'svokmno', 'sinsmno', 'slokmno'
    ];
    for (const vid of this.pridev.vidovi) {
      for (const prop of properties) {
        if (vid.hasOwnProperty(prop)) {
          if (vid[prop]) {
            return false;
          }
        }
      }
    }
    return true;
  }

  check(): boolean {
    try {
      this.assert(this.allEmpty(), 'Ниједан облик није попуњен!');
      return true;
    } catch (e) {
      return false;      
    }
  }

  save(): void {
    if (!this.check()) return;
    if (!this.editMode) {
      this.pridevService.add(this.pridev).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Придев је успешно сачуван.`,
          });
          this.router.navigate(['/pridev', data.id]);
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
      this.pridevService.update(this.pridev).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Придев је успешно сачуван.`,
          });
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
    if (this.tokenStorageService.getUser().id === this.pridev.vlasnikID)
      return true;
    return false;
  }
}

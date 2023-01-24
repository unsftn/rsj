import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
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
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Придев');
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
    this.refocus();
  }

  refocus(): void {
    setTimeout(() => { this.textInput.nativeElement.focus(); }, 0);
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
      'monomjed', 'mogenjed',  'modatjed',  'moakujed',  'movokjed',  'moinsjed',  'molokjed',  'monommno',  'mogenmno',  
      'modatmno',  'moakumno',  'movokmno',  'moinsmno',  'molokmno',  'mnnomjed',  'mngenjed',  'mndatjed',  'mnakujed',  
      'mnvokjed',  'mninsjed',  'mnlokjed',  'mnnommno',  'mngenmno',  'mndatmno',  'mnakumno',  'mnvokmno',  'mninsmno',  
      'mnlokmno',  'mknomjed',  'mkgenjed',  'mkdatjed',  'mkakujed',  'mkvokjed',  'mkinsjed',  'mklokjed',  'mknommno',  
      'mkgenmno',  'mkdatmno',  'mkakumno',  'mkvokmno',  'mkinsmno',  'mklokmno',  'msnomjed',  'msgenjed',  'msdatjed',  
      'msakujed',  'msvokjed',  'msinsjed',  'mslokjed',  'msnommno',  'msgenmno',  'msdatmno',  'msakumno',  'msvokmno',  
      'msinsmno',  'mslokmno',  'zpnomjed',  'zpgenjed',  'zpdatjed',  'zpakujed',  'zpvokjed',  'zpinsjed',  'zplokjed',  
      'zpnommno',  'zpgenmno',  'zpdatmno',  'zpakumno',  'zpvokmno',  'zpinsmno',  'zplokmno',  'zknomjed',  'zkgenjed',  
      'zkdatjed',  'zkakujed',  'zkvokjed',  'zkinsjed',  'zklokjed',  'zknommno',  'zkgenmno',  'zkdatmno',  'zkakumno',  
      'zkvokmno',  'zkinsmno',  'zklokmno',  'zsnomjed',  'zsgenjed',  'zsdatjed',  'zsakujed',  'zsvokjed',  'zsinsjed',  
      'zslokjed',  'zsnommno',  'zsgenmno',  'zsdatmno',  'zsakumno',  'zsvokmno',  'zsinsmno',  'zslokmno',  'spnomjed',  
      'spgenjed',  'spdatjed',  'spakujed',  'spvokjed',  'spinsjed',  'splokjed',  'spnommno',  'spgenmno',  'spdatmno',  
      'spakumno',  'spvokmno',  'spinsmno',  'splokmno',  'sknomjed',  'skgenjed',  'skdatjed',  'skakujed',  'skvokjed',  
      'skinsjed',  'sklokjed',  'sknommno',  'skgenmno',  'skdatmno',  'skakumno',  'skvokmno',  'skinsmno',  'sklokmno',  
      'ssnomjed',  'ssgenjed',  'ssdatjed',  'ssakujed',  'ssvokjed',  'ssinsjed',  'sslokjed',  'ssnommno',  'ssgenmno',  
      'ssdatmno',  'ssakumno',  'ssvokmno',  'ssinsmno',  'sslokmno'];
    for (const prop of properties) {
      if (this.pridev.hasOwnProperty(prop)) {
        if (this.pridev[prop].trim()) {
          return false;
        }
      }
    }
    return true;
  }

  allNominative(): boolean {
    // let properties = [ 
    //   'monomjed', 'monommno', 'mknomjed', 'mknommno', 'msnomjed', 'msnommno', 
    //   'zpnomjed', 'zpnommno', 'zknomjed', 'zknommno', 'zsnomjed', 'zsnommno',
    //   'spnomjed', 'spnommno', 'sknomjed', 'sknommno', 'ssnomjed', 'ssnommno',
    // ];
    let properties = [ 
      'monomjed', 'monommno', 'zpnomjed', 'zpnommno', 'spnomjed', 'spnommno', 
    ];
    if (this.pridev.dvaVida)
      // properties.push('mnnomjed', 'mnnommno');
      properties.push('mnnomjed');
    for (const prop of properties) {
      if (this.pridev.hasOwnProperty(prop)) {
        if (!this.pridev[prop].trim()) {
          return false;
        }
      }
    }
    return true;
  }

  emptyVariants(): boolean {
    let properties = [
      'onomjed', 'ogenjed', 'odatjed', 'oakujed', 'ovokjed', 'oinsjed', 'olokjed', 'nnomjed', 'ngenjed',
      'ndatjed', 'nakujed', 'nvokjed', 'ninsjed', 'nlokjed', 'pnomjed', 'pgenjed', 'pdatjed', 'pakujed',
      'pvokjed', 'pinsjed', 'plokjed', 'knomjed', 'kgenjed', 'kdatjed', 'kakujed', 'kvokjed', 'kinsjed',
      'klokjed', 'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed'
    ];
    for (const v of this.pridev.varijante) {
      let empty = true;
      for (const prop of properties) {
        if (v.hasOwnProperty(prop)) {
          if (v[prop].trim())
            empty = false;
        }
      }
      if (empty)
        return true;
    }
    return false;
  }

  check(): boolean {
    try {
      this.assert(this.allEmpty(), 'Ниједан облик није попуњен!');
      this.assert(!this.allNominative(), 'Номинатив је обавезан у свим родовима једнине и множине!');
      this.assert(this.emptyVariants(), 'Постоји бар једна потпуно празна варијанта!');
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

  addVarijanta(rod: number): void {
    const redni_broj = this.pridev.varijante.length + 1;
    const varijanta = this.pridevService.newVarijanta(rod, redni_broj);
    this.pridev.varijante.push(varijanta);
  }

  moveUp(index: number): void {
    if (index === 0)
      return;
    const temp = this.pridev.varijante.splice(index, 1)[0];
    this.pridev.varijante.splice(index - 1, 0, temp);
  }

  moveDown(index: number): void {
    if (index === this.pridev.varijante.length - 1)
      return;
    const temp = this.pridev.varijante.splice(index, 1)[0];
    this.pridev.varijante.splice(index + 1, 0, temp);
  }

  remove(index: number): void {
    this.pridev.varijante.splice(index, 1);
  }

  varTabOffset(index: number): number {
    const neodredjeniCount = this.pridev.dvaVida ? 7 : 0;
    return 56 + index * (21 + neodredjeniCount);
  }

  saveAvailable() {
    if (this.tokenStorageService.isEditor())
      return true;
    if (!this.editMode)
      return true;
    if (this.pridev.vlasnikID === 3)
      return true;  // izmena prideva je dozvoljena ako je autor WikiMorph_sr
    if (this.tokenStorageService.getUser().id === this.pridev.vlasnikID)
      return true;
    return false;
  }
}

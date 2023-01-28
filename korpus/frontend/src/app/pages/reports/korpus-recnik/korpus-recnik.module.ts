import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { DropdownModule } from 'primeng/dropdown';
import { MultiSelectModule } from 'primeng/multiselect';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { InputNumberModule } from 'primeng/inputnumber';
import { DialogModule } from 'primeng/dialog';
import { KorpusRecnikComponent } from './korpus-recnik.component';

const routes: Routes = [{ path: '', component: KorpusRecnikComponent }]

@NgModule({
  declarations: [
    KorpusRecnikComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    DropdownModule,
    MultiSelectModule,
    ButtonModule,
    RippleModule,
    InputNumberModule,
    DialogModule,
  ],
  exports: [RouterModule],
  bootstrap: [KorpusRecnikComponent]
})
export class KorpusRecnikModule { }

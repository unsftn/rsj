import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { Table, TableModule } from 'primeng/table';
import { ReferencaComponent } from './referenca.component';


@NgModule({
  declarations: [ReferencaComponent],
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    RippleModule,
    AutoCompleteModule,
    TableModule,
  ],
  exports: [ReferencaComponent],
  providers: [],
  bootstrap: [ReferencaComponent]
})
export class ReferencaModule { }

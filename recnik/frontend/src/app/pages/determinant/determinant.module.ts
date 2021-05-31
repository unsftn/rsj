import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { TagModule } from 'primeng/tag';
import { InputTextModule } from 'primeng/inputtext';
import { DeterminantComponent } from './determinant.component';

@NgModule({
  declarations: [DeterminantComponent],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    ButtonModule,
    AutoCompleteModule,
    TagModule,
    InputTextModule,
    RippleModule,
  ],
  exports: [DeterminantComponent],
  providers: [],
  bootstrap: [DeterminantComponent],
})
export class DeterminantModule {}

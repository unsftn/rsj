import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { DeterminantComponent } from './determinant.component';

import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [DeterminantComponent],
  imports: [
    FormsModule,
    AutoCompleteModule,
    CommonModule,
    ButtonModule,
    HttpClientModule,
  ],
  exports: [DeterminantComponent],
  providers: [],
  bootstrap: [DeterminantComponent],
})
export class DeterminantModule {}

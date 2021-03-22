import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
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
  ],
  exports: [DeterminantComponent],
  providers: [],
  bootstrap: [DeterminantComponent],
})
export class DeterminantModule {}

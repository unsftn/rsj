import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { HttpClientModule } from '@angular/common/http';
// import { DeterminantModule } from '../determinant/determinant.module';
import { ReferencaModule } from '../referenca/referenca.module';
import { SynonymComponent } from './synonym.component';

@NgModule({
  declarations: [SynonymComponent],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    ButtonModule,
    AutoCompleteModule,
    // DeterminantModule,
    ReferencaModule,
  ],
  exports: [SynonymComponent],
  providers: [],
  bootstrap: [SynonymComponent],
})
export class SynonymModule {}

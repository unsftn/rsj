import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AntonymComponent } from './antonym.component';

import { AutoCompleteModule } from 'primeng/autocomplete';
import { ButtonModule } from 'primeng/button';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [AntonymComponent],
  imports: [
    FormsModule,
    AutoCompleteModule,
    CommonModule,
    ButtonModule,
    HttpClientModule,
  ],
  exports: [AntonymComponent],
  providers: [],
  bootstrap: [AntonymComponent],
})
export class AntonymModule {}

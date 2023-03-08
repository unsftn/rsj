import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { BrojComponent } from './broj.component';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';

const routes: Routes = [{ path: '', component: BrojComponent }]

@NgModule({
  declarations: [BrojComponent],
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    MyToolbarModule,
    PossibleDupeModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [BrojComponent]
})
export class BrojModule { }

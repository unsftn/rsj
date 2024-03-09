import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { ButtonModule } from 'primeng/button';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';
import { AreYouSureModule } from '../../are-you-sure/are-you-sure.module';
import { BrojComponent } from './broj.component';

const routes: Routes = [{ path: '', component: BrojComponent }]

@NgModule({
  declarations: [BrojComponent],
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    ButtonModule,
    MyToolbarModule,
    PossibleDupeModule,
    AreYouSureModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [BrojComponent]
})
export class BrojModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FileUploadModule } from 'primeng/fileupload';
import { OrderListModule } from 'primeng/orderlist';
import { TimelineModule } from 'primeng/timeline';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { MainImportComponent } from './main-import/main-import.component';
import { SelectFilesComponent } from './select-files/select-files.component';
import { ProcessStepComponent } from './process-step/process-step.component';

const routes: Routes = [
  {
    path: '',
    component: MainImportComponent,
    children: [{
      path: '',
      redirectTo: 'datoteke',
      pathMatch: 'full'
    }, {
      path: 'datoteke',
      component: SelectFilesComponent,
      data: { title: 'Избор датотека' }
    }]
  }
];

@NgModule({
  declarations: [SelectFilesComponent, ProcessStepComponent, MainImportComponent],
  imports: [
    CommonModule,
    FileUploadModule,
    OrderListModule,
    TimelineModule,
    ToolbarModule,
    ConfirmDialogModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [MainImportComponent]
})
export class ImporterModule { }

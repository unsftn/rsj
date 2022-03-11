import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FileUploadModule } from 'primeng/fileupload';
import { OrderListModule } from 'primeng/orderlist';
import { TimelineModule } from 'primeng/timeline';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService } from 'primeng/api';
import { TableModule } from 'primeng/table';
import { MainImportComponent } from './main-import/main-import.component';
import { SelectFilesComponent } from './select-files/select-files.component';
import { ProcessStepComponent } from './process-step/process-step.component';
import { ExtractionComponent } from './extraction/extraction.component';
import { TagModule } from 'primeng/tag';

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
    }, {
      path: 'ekstrakcija',
      component: ExtractionComponent,
      data: { title: 'Издвајање текста' }
    }]
  }
];

@NgModule({
  declarations: [SelectFilesComponent, ProcessStepComponent, MainImportComponent, ExtractionComponent],
  imports: [
    CommonModule,
    FileUploadModule,
    OrderListModule,
    TimelineModule,
    ToolbarModule,
    ConfirmDialogModule,
    TableModule,
    TagModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  providers: [ConfirmationService],
  bootstrap: [MainImportComponent]
})
export class ImporterModule { }

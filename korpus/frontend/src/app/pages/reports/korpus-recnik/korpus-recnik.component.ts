import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { DeciderService } from '../../../services/decider/decider.service';

@Component({
  selector: 'app-korpus-recnik',
  templateUrl: './korpus-recnik.component.html',
  styleUrls: ['./korpus-recnik.component.scss']
})
export class KorpusRecnikComponent implements OnInit {

  dane: any[] = [
    { name: '---', value: null },
    { name: 'да', value: true },
    { name: 'не', value: false }
  ];

  sveOdluke: any[] = [
    { name: 'без одлуке', value: 1 },
    { name: 'иде у речник', value: 2 },
    { name: 'не иде у речник', value: 3 },
    { name: 'иде у проширени речник', value: 4 },
    { name: 'уклони из речника', value: 5 }
  ];

  svaSlova: any[] = [
    { name: 'а', value: 'а' },
    { name: 'б', value: 'б' },
    { name: 'в', value: 'в' },
    { name: 'г', value: 'г' },
    { name: 'д', value: 'д' },
    { name: 'ђ', value: 'ђ' },
    { name: 'е', value: 'е' },
    { name: 'ж', value: 'ж' },
    { name: 'з', value: 'з' },
    { name: 'и', value: 'и' },
    { name: 'ј', value: 'ј' },
    { name: 'к', value: 'к' },
    { name: 'л', value: 'л' },
    { name: 'љ', value: 'љ' },
    { name: 'м', value: 'м' },
    { name: 'н', value: 'н' },
    { name: 'њ', value: 'њ' },
    { name: 'о', value: 'о' },
    { name: 'п', value: 'п' },
    { name: 'р', value: 'р' },
    { name: 'с', value: 'с' },
    { name: 'т', value: 'т' },
    { name: 'ћ', value: 'ћ' },
    { name: 'у', value: 'у' },
    { name: 'ф', value: 'ф' },
    { name: 'х', value: 'х' },
    { name: 'ц', value: 'ц' },
    { name: 'ч', value: 'ч' },
    { name: 'џ', value: 'џ' },
    { name: 'ш', value: 'ш' },
  ];

  uRecniku: any;
  uKorpusu: any;
  frekOd: number;
  frekDo: number;
  odluke: any[];
  slova: any[];
  formDisabled: boolean;
  areYouSure: boolean;
  mustChoose: boolean;
  reportTimer: any;
  reportId: number;
  pleaseWait: boolean;

  constructor(
    private title: Title,
    private deciderService: DeciderService,
  ) {}

  ngOnInit(): void {
    this.title.setTitle('Извештаји из корпуса');
    this.formDisabled = false;
    this.areYouSure = false;
    this.mustChoose = false;
    this.uRecniku = this.dane[0];
    this.uKorpusu = this.dane[0];
    this.frekOd = null;
    this.frekDo = null;
    this.odluke = [];
    this.slova = [];
    this.reportId = null;
    this.pleaseWait = false;
  }

  generisi(): void {
    if (!this.check()) {
      this.mustChoose = true;
      return;
    }
    this.formDisabled = true;
    this.areYouSure = true;
  }

  da(): void {
    this.areYouSure = false;
    this.reportId = null;
    this.sendReportRequest();
  }

  ne(): void {
    this.areYouSure = false;
    this.formDisabled = false;
  }

  ok(): void {
    this.mustChoose = false;
  }

  check(): boolean {
    return (this.uKorpusu.value !== null) || 
      (this.uRecniku.value !== null) || 
      (this.frekOd !== null) || 
      (this.frekDo !== null) || 
      (this.odluke.length > 0) || 
      (this.slova.length > 0);
  }

  getParams(): any {
    return {
      u_korpusu: this.uKorpusu.value,
      u_recniku: this.uRecniku.value,
      frek_od: this.frekOd,
      frek_do: this.frekDo,
      odluke: this.odluke,
      slova: this.slova
    }
  }

  sendReportRequest(): void {
    this.pleaseWait = true;
    this.deciderService.createReport(this.getParams()).subscribe({
      next: (reportId: number) => {
        this.reportTimer = setInterval(() => { 
          this.updateReportStatus(reportId);
        }, 3000);
      },
      error: (error: any) => console.log(error)
    });
  }

  updateReportStatus(reportId: number): void {
    this.deciderService.getReport(reportId).subscribe({
      next: (report: any) => {
        if (report.zavrsen) {
          clearInterval(this.reportTimer);
          this.pleaseWait = false;
          this.formDisabled = false;
          this.reportId = report.id;
        }
      },
      error: (error: any) => console.log(error)
    });
  }

  download(): void {
    if (this.reportId) {
      // TODO: download PDF
    }
  }

}

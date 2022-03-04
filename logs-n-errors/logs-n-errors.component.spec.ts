import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogsNErrorsComponent } from './logs-n-errors.component';

describe('LogsNErrorsComponent', () => {
  let component: LogsNErrorsComponent;
  let fixture: ComponentFixture<LogsNErrorsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LogsNErrorsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LogsNErrorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
